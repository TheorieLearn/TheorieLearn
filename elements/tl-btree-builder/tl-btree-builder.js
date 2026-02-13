var canvas;

var caretTimer;
var caretVisible = true;
var cursorVisible = true;
var movingObject = false;
var selectedObject = null;
var selectedIndex = 0;
var tempObj = null;
var originalClick;

const snapToPadding = 6; // pixels
const hitTargetPadding = 6; // pixels

// For the backend tree structure in both modes. Equivalent to the python dicts.
var backend = null;

// These represent the frontend tree structure in both modes
var nodes = [];
var root = null;
var links = [];

var answersName = null;

let smallX = 26
let smallY = 39
let largeX = 40
let largeY = 60
var nodeXSidelength = largeX;
var nodeYSidelength = largeY;
var buttonSideLength = 13;
var nextBacknodeId = 0;
var squareButtons = [];

var layerSpacingArr = [];
var sublayersToAddPerLayer = [0];
var subLayerCount = 0;

var shift = false;
var ctrl = false;
var alt = false;
var downkey = false;
var numeric_input_only = false;
var canEdit = true;

// Helper Functions From https://gist.github.com/janosh/099bd8061f15e3fbfcc19be0e6b670b9
const argFact = (compareFn) => (array) => array.map((el, idx) => [el, idx]).reduce(compareFn)[1];
const argMax = argFact((min, el) => (el[0] > min[0] ? el : min));
const argMin = argFact((max, el) => (el[0] < max[0] ? el : max));

function tree_builder_init(name, starterBackend, backendTreeJson, editable, numeric_input, small_start){
    // Get canvas from page and initialize context.
    answersName = name;
    canvas = document.getElementById(answersName + '-tree-canvas')

    numeric_input_only = numeric_input

    if (backendTreeJson == null || backendTreeJson == "") {
        backendTreeJson = '{"value": [""],"children": []}';
    }
    canEdit = editable;
    if (small_start) {
        nodeXSidelength = smallX;
        nodeYSidelength = smallY;
    }

    restoreBackendJson(backendTreeJson);
    draw();

    canvas.onmousedown = function (e) {
        // Get mouse position and select object if possible.
        var mouse = crossBrowserRelativeMousePos(e);
        selectedObject = selectObject(mouse.x, mouse.y);
        movingObject = false;
        originalClick = mouse;

        if (selectedObject != null) {

            if (selectedObject instanceof SquareButton) {
                if (selectedObject.type == "add") {
                    addNewNodeElementWrapper(selectedObject.id, selectedObject.isLeft, selectedObject.index);
                } else if (selectedObject.type == "del") {
                    RemoveNodeElementWrapper(selectedObject.id, selectedObject.index);
                } else if (selectedObject.type == "pro") {
                    promoteElementWrapper(selectedObject.id, selectedObject.index);
                } else if (selectedObject.type == "dem") {
                    demoteElementWrapper(selectedObject.id, selectedObject.index);
                }
            }
            resetCaret();
        }

        draw();


        if (canvasHasFocus()) {
            // disable drag-and-drop only if the canvas is already focused
            return false;
        } else {
            // otherwise, let the browser switch the focus away from wherever it was
            resetCaret();
            return true;
        }
    };

    $('#' + answersName + '-clear-tree').on('click', () => {
        if (window.confirm('Are you sure you want to reset your tree?')) {
            if (starterBackend == null || starterBackend == "") {
                starterBackend = '{"value": [""],"children": []}';
            }
            restoreBackendJson(starterBackend);
            draw();
        }
    });

    $('#' + answersName + '-toggle-state-size').on('click', () => {
        if (nodeXSidelength == smallX) {
            nodeXSidelength = largeX
            nodeYSidelength = largeY
        } else {
            nodeXSidelength = smallX
            nodeYSidelength = smallY
        }
        processBackendJson()
        draw();
    });
}

// Handles keys, mainly for keyboard shortcuts. Separate from document.onkeypress which handles most typing
// registers ctrl / shift / alt being pressed
// Handles arrowkey shortcuts
// Handles backspace shortcut and text deleting.
document.onkeydown = function (e) {
    var key = crossBrowserKey(e);
    if (!canvasHasFocus()) {
        // don't read keystrokes when other things have focus
        return true;
    } else if (key == 16) { // shift key
        shift = true
    } else if (key == 17) { // ctrl key
        ctrl = true;
    } else if (key == 18) { // alt key
        alt = true
    } else if (key == 37) { // arrowleft
        if (selectedObject instanceof Node) {
            if (ctrl && selectedObject.canAddNodes) {
                addNewNodeElementWrapper(selectedObject.id, true, selectedIndex);
            } else if (downkey && selectedObject.wouldDemoteNodes) {
                bnode = findBackendNodeByID(selectedObject.id)
                selectedObject = findDrawnNodeById(bnode.children[selectedIndex].id)
                selectedIndex = 0
            } else {
                selectedIndex = ((selectedIndex - 1) + selectedObject.text.length) % selectedObject.text.length
            }
        }
        return false
    } else if (key == 38) { // arrowup
        if (selectedObject instanceof Node) {
            if (ctrl && selectedObject.canPromoteNodes) {
                promoteElementWrapper(selectedObject.id, selectedIndex);
            } else {
                bnode = findBackendNodeByID(selectedObject.id)
                bp = bnode.parentId
                bpind = bnode.parentIndex
                if (bp != -1) {
                    selectedObject = findDrawnNodeById(bp)
                    selectedIndex = bpind == selectedObject.text.length ? bpind - 1 : bpind
                }
            }
        }
        return false
    } else if (key == 39) { // arrowright
        if (selectedObject instanceof Node) {
            if (ctrl && selectedObject.canAddNodes) {
                addNewNodeElementWrapper(selectedObject.id, false, selectedIndex);
            } else if (downkey && selectedObject.wouldDemoteNodes) {
                bnode = findBackendNodeByID(selectedObject.id)
                selectedObject = findDrawnNodeById(bnode.children[selectedIndex + 1].id)
                selectedIndex = 0
            }else {
                selectedIndex = (selectedIndex + 1) % selectedObject.text.length
            }
        }
        return false
    } else if (key == 40) { // arrowdown
        if (selectedObject instanceof Node) {
            if (ctrl && selectedObject.canDemoteNodes) {
                demoteElementWrapper(selectedObject.id, selectedIndex);
            }
        }
        downkey = true;
        return false
    } else if (key == 8) { // backspace key
        if (selectedObject instanceof Node && ctrl && selectedObject.canDeleteNodes) {
            RemoveNodeElementWrapper(selectedObject.id, selectedIndex)
        } else if (selectedObject != null && 'text' in selectedObject && canEdit) {
            selectedObject.text[selectedIndex] = selectedObject.text[selectedIndex].substr(0, selectedObject.text[selectedIndex].length - 1);
            resetCaret();
            draw();
        }

        // backspace is a shortcut for the back button, but do NOT want to change pages
        return false;
    }
};

// Other key handler, separate from document.onkeydown()
// Allows us to type in nodes when we're typing a legal character, we can edit, the right object is selected, etc.
document.onkeypress = function (e) {
    if (canEdit) {
        // don't read keystrokes when other things have focus
        var key = crossBrowserKey(e);
        keyBounds = false

        if (selectedObject instanceof Node) {
            if (numeric_input_only) {
                keyBounds = (key >= 48 && key <= 57)
            } else {
                keyBounds = (key >= 0x20 && key <= 0x7E)
            }
        }
        if (!canvasHasFocus()) {
            // don't read keystrokes when other things have focus
            return true;

        } else if (keyBounds && !e.metaKey && !e.altKey && !e.ctrlKey && selectedObject != null && 'text' in selectedObject) {
            // Reset highlighting when user types

            selectedObject.text[selectedIndex] += String.fromCharCode(key);
            resetCaret();
            draw();

            // don't let keys do their actions (like space scrolls down the page)
            return false;
        } else if (key == 8) {
            // backspace is a shortcut for the back button, but do NOT want to change pages
            return false;
        }
    }
};

// Undoes anything that could be used for a press+hold shortcutS
document.onkeyup = function (e) {
    var key = crossBrowserKey(e);

    if (key == 17) { // ctrl key
        ctrl = false;
    } else if (key == 16) {
        shift = false
    } else if (key == 18) {
        alt = false
    } else if (key == 40) {
        downkey = false
    }
};

// Redraw the frontend. Requires all front end objects to have been created and stored in the arrays
// links, nodes, and squarebuttons.
// selectedObject and selectedIndex are accessed to affect highlighting.
// wrapper for drawUsing
function draw() {
    drawUsing(canvas.getContext('2d'));
    saveBackup();
}

function drawUsing(c){
    c.clearRect(0, 0, canvas.width, canvas.height);
    c.save();

    // Because of how the current highlighting works, links MUST be drawn before nodes.
    for (var i = 0; i < links.length; i++){
        links[i].draw(c);
    }

    for (var i = 0; i < nodes.length; i++){
        c.lineWidth = 1;
        nodes[i].draw(c);
    }

    for (var i = 0; i < squareButtons.length; i++) {
        c.lineWidth = 1;
        squareButtons[i].draw(c);
    }

    if (tempObj){
        c.lineWidth = 1;
        c.fillStyle = c.strokeStyle = 'black'
        tempObj.draw(c);
    }
}

// returns object to be placed in selectedObject.
// also redefines selectedIndex if applicable
function selectObject(x, y) {
    for (var i = 0; i < squareButtons.length; i++) {
        if (squareButtons[i].containsPoint(x, y)) {
            return squareButtons[i];
        }
    }

    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].containsPoint(x, y)) {
            selectedIndex = nodes[i].indexContainsPoint(x);
            return nodes[i];
        }
    }
    return null;
}

function drawText(c, originalText, x, y, angleOrNull, isSelected) {
    text = originalText
    //text = convertLatexShortcuts(originalText);
    c.font = '20px "Times New Roman", serif';
    var width = c.measureText(text).width;

    // Attempt to keep text within the bounds of the node
    if (width > nodeXSidelength + 2) {
        var newpx = 20 - parseInt((width - nodeXSidelength) / 8);
        if (newpx < 10) newpx = 10;
        c.font = newpx + 'px "Times New Roman", serif';
        width = c.measureText(text).width;
    }

    // center the text
    x -= width / 2;

    // position the text intelligently if given an angle
    if (angleOrNull != null) {
        var cos = Math.cos(angleOrNull);
        var sin = Math.sin(angleOrNull);
        var cornerPointX = (width / 2 + 5) * (cos > 0 ? 1 : -1);
        var cornerPointY = (10 + 5) * (sin > 0 ? 1 : -1);
        var slide = sin * Math.pow(Math.abs(sin), 40) * cornerPointX - cos * Math.pow(Math.abs(cos), 10) * cornerPointY;
        x += cornerPointX - sin * slide;
        y += cornerPointY + cos * slide;
    }

    // draw text and caret (round the coordinates so the caret falls on a pixel)
    if ('advancedFillText' in c) {
        c.advancedFillText(text, originalText, x + width / 2, y, angleOrNull);
    } else {
        x = Math.round(x);
        y = Math.round(y);
        c.fillText(text, x, y + 6);
        if (isSelected && caretVisible && canvasHasFocus() && document.hasFocus() && canEdit) {
            x += width;
            c.beginPath();
            c.moveTo(x, y - 10);
            c.lineTo(x, y + 10);
            c.stroke();
        }
    }
}

function snapNode(node) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i] == node) continue;

        if (Math.abs(node.x - nodes[i].x) < snapToPadding) {
            node.x = nodes[i].x;
        }

        if (Math.abs(node.y - nodes[i].y) < snapToPadding) {
            node.y = nodes[i].y;
        }
    }
}

function canvasHasFocus() {
    return (document.activeElement || document.body) == document.body;
}

function resetCaret() {
    clearInterval(caretTimer);
    caretTimer = setInterval('caretVisible = !caretVisible; draw()', 500);
    caretVisible = true;
}

function crossBrowserKey(e) {
    e = e || window.event;
    return e.which || e.keyCode;
}

function crossBrowserRelativeMousePos(e) {
    var element = crossBrowserElementPos(e);
    var mouse = crossBrowserMousePos(e);
    return {
        'x': mouse.x - element.x,
        'y': mouse.y - element.y
    };
}

function crossBrowserMousePos(e) {
    e = e || window.event;
    return {
        'x': e.pageX || e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft,
        'y': e.pageY || e.clientY + document.body.scrollTop + document.documentElement.scrollTop,
    };
}

function crossBrowserElementPos(e) {
    e = e || window.event;
    var obj = e.target || e.srcElement;
    var x = 0, y = 0;
    while (obj.offsetParent) {
        x += obj.offsetLeft;
        y += obj.offsetTop;
        obj = obj.offsetParent;
    }
    return { 'x': x, 'y': y };
}

function drawArrow(c, x, y, angle) {
    var dx = Math.cos(angle);
    var dy = Math.sin(angle);
    c.beginPath();
    c.moveTo(x, y);
    c.lineTo(x - 8 * dx + 5 * dy, y - 8 * dy - 5 * dx);
    c.lineTo(x - 8 * dx - 5 * dy, y - 8 * dy + 5 * dx);
    c.moveTo(x,y);
    c.fill();
}

// This function handles what we return for grading
// Currently all that is required is the backend tree
function saveBackup() {
    if (!JSON){
        return;
    }

    var parentTemp = [];

    for (var i = 0; i < nodes.length; i++) {
        parentTemp.push(nodes[i].parent);
        nodes[i].parent = null;
    }

    updateBackendText()

    var backup = {
        'backendRoot': backend
    }

    $('input#' + answersName + '-raw-json').val(JSON.stringify(backup));


    for (var i = 0; i < nodes.length; i++) {
        nodes[i].parent = parentTemp[i];
    }
}

// Given an id (assigned to all backend nodes, frontend nodes, and frontend squarebuttons to maintain consistency)
// returns the frontend node associated
// backend version in findBackendNodeById
function findDrawnNodeById(id) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].id == id) {
            return nodes[i];
        }
    }
}

// When the student types it only directly affects the front end.
// This moves the data from the front to the back so it remains stored
function updateBackendText() {
    updateBackendTextNode(backend);
}
function updateBackendTextNode(backnode) {
    if (backnode == null) {
        return;
    }
    var drawnNode = findDrawnNodeById(backnode.id);
    backnode.value = drawnNode.text;
    for (var i = 0; i < backnode.children.length; i++) {
        updateBackendTextNode(backnode.children[i]);
    }
}

// Specifically this takes the backend json that was inputted to the file -> which is a JSON rendering of the python dict
// created by BtreeNode object in btreenode.utils.py.
// Does extra processing (parsing json and assigning ids) before calling processBackendJson
function restoreBackendJson(backendJson) {
    if (!backendJson) {
        backend = null;
    }
    try {
        var beclean = backendJson.replace(/'/g, '"');
        var beclean2 = beclean.replace(/None/g, "null");
        var beclean3 = beclean2.replace(/False/g, 'false');
        var beclean4 = beclean3.replace(/True/g, 'true');
        backend = JSON.parse(beclean4)
    } catch (e) {
        console.log(e)
        return;
    }
    populateBackendIds(backend);
    processBackendJson();
}

// Goes through the backend tree and assigns ids, assuming none of them have ids. This typically only needs to be called at the beginng,
// as single ids can be assigned when creating a new node.
function populateBackendIds(bnode, parentId=-1, index=0) {
    if (bnode) {
        bnode.id = nextBacknodeId;
        bnode.parentId = parentId;
        bnode.parentIndex = index;
        nextBacknodeId++;
        for (var i = 0; i < bnode.children.length; i++) {
            populateBackendIds(bnode.children[i], bnode.id, i);
        }
    }
}

// Given an id (assigned to all backend nodes, frontend nodes, and frontend squarebuttons to maintain consistency)
// returns the backend node associated
// frontend version findDrawnNodeById
function findBackendNodeByID(id) {
    return findBackendNodeByIDInternal(backend, id)
}
function findBackendNodeByIDInternal(backnode, id) {
    if (!backnode) {
        return null;
    }
    if (backnode.id == id) {
        return backnode;
    } else {
        for (var i = 0; i < backnode.children.length; i++) {
            node = findBackendNodeByIDInternal(backnode.children[i], id)
            if (node) {
                return node
            }
        }
        return null
    }
}

// Takes the given node, and iterates through it, giving all children the parentId = to the given node.
// also updates all the children's parent index
// Works at one level - no recursion
function updateChildParentIds(node) {
    newId = node.id
    const mapper = (child, index) => {
        child.parentId = newId;
        child.parentIndex = index;
    }
    node.children.map(mapper)
}

// Given a node's id and the index, promotes the element, splitting nodes, reassigning children, and either creating a new node
// or adding the element to parent. reassigns the 'backend' variable as necessary.
// updates backend then frontend and redraws.
// selects the newly promoted element afterwards
function promoteElementWrapper(promoteNodeId, promoteIndex) {
    updateBackendText();
    retidind = promoteElement(promoteNodeId, promoteIndex);
    processBackendJson();
    selectedObject = findDrawnNodeById(retidind[0])
    selectedIndex = retidind[1]
    draw();
}

function promoteElement(promoteNodeId, promoteIndex) {
    backnode = findBackendNodeByID(promoteNodeId)
    if (!backnode) {return}

    var leftChildNode = {value: backnode.value.slice(0,promoteIndex),
        children: backnode.children.slice(0,promoteIndex + 1),
        id: backnode.id};
    var rightChildNode = {value: backnode.value.slice(promoteIndex + 1),
        children: backnode.children.slice(promoteIndex + 1),
        id: nextBacknodeId};
    nextBacknodeId++
    updateChildParentIds(rightChildNode)

    var retidind = [0,0]
    if (backnode.parentId == -1) {
        var newParentNode = {value: [backnode.value[promoteIndex]],
            children: [leftChildNode, rightChildNode],
            id: nextBacknodeId,
            parentId: -1,
        };
        nextBacknodeId++;
        updateChildParentIds(newParentNode)

        backend = newParentNode
        retidind = [newParentNode.id, 0]
    } else {
        var parentNode = findBackendNodeByID(backnode.parentId);
        let pi = backnode.parentIndex
        parentNode.value.splice(pi, 0, backnode.value[promoteIndex])
        parentNode.children.splice(pi, 1, leftChildNode, rightChildNode)
        updateChildParentIds(parentNode)
        retidind = [parentNode.id, pi]
    }
    return retidind
}

// demotes element and combines children nodes.
// handles all cases where destroying nodes or reassigning children to parents may be necessary.
// updates backend, frontend, and redraws
// selects the element that was newly demoted.
function demoteElementWrapper(demoteNodeId, demoteIndex) {
    updateBackendText();
    retidind = demoteElement(demoteNodeId, demoteIndex);
    processBackendJson();
    selectedObject = findDrawnNodeById(retidind[0])
    selectedIndex = retidind[1]
    draw();
}

function demoteElement(demoteNodeId, demoteIndex) {
    backnode = findBackendNodeByID(demoteNodeId)
    if (!backnode) {return}

    let leftnode = backnode.children[demoteIndex]
    let rightnode = backnode.children[demoteIndex + 1]
    var newNode = {value: leftnode.value.concat([backnode.value[demoteIndex]], rightnode.value),
        children: leftnode.children.concat(rightnode.children),
        id: nextBacknodeId,
        parentId: backnode.parentId,
    }
    let retidind = [newNode.id, leftnode.value.length]
    nextBacknodeId++;
    updateChildParentIds(newNode)

    if (backnode.value.length == 1) {
        if (backnode.parentId == -1) {
            newNode.parentIndex = 0
            backend = newNode
        } else {
            parentNode = findBackendNodeByID(backnode.parentId)
            parentNode.children[backnode.parentIndex] = newNode
            updateChildParentIds(parentNode)
        }
    } else {
        backnode.value.splice(demoteIndex, 1)
        backnode.children.splice(demoteIndex, 2, newNode)
        updateChildParentIds(backnode)
    }
    return retidind
}

// Adds an element within a given node, initializes value to empty string. selects new element.
function addNewNodeElementWrapper(newNodeId, newNodeIsLeft, newNodeIndex) {
    updateBackendText();
    let trueNodeIndex = newNodeIndex + (newNodeIsLeft ? 0 : 1)
    addNewNodeElement(backend, newNodeId, trueNodeIndex);
    processBackendJson();
    selectedObject = findDrawnNodeById(newNodeId)
    selectedIndex = trueNodeIndex
    draw();
}

function addNewNodeElement(backnode, newNodeId, newNodeIndex) {

    if (!backnode) {
        return false;
    }
    if (backnode.id == newNodeId) {
        backnode.value.splice(newNodeIndex, 0, "")
        return true;
    } else {
        const recursivecall = (child) => {return addNewNodeElement(child, newNodeId, newNodeIndex)}
        return (backnode.children.some(recursivecall));
    }
}

// Remove an element from a given node. Selects node to the left of deleted one.
function RemoveNodeElementWrapper(removeNodeId, index) {
    updateBackendText();
    RemoveNodeElement(backend, removeNodeId, index);
    processBackendJson();
    selectedObject = findDrawnNodeById(removeNodeId)
    selectedIndex = index == 0 ? 0 : index - 1
    draw();
}

function RemoveNodeElement(backnode, removeNodeId, index) {
    if (!backnode) {
        return false;
    }
    if (backnode.id == removeNodeId) {
        backnode.value.splice(index, 1)
        return true;
    } else {
        const recursivecall = (child) => {return RemoveNodeElement(child, removeNodeId, index)}
        return (backnode.children.some(recursivecall));
    }
}

// Populates the .layer and .sublayer fields for every node
// returns ret[layer #][sublayer #] = the gaps between nodes for this sublevel.
// Therefore inherently includes count of layers and sublayers
// All nodes the same number of jumps from the root are at the same 'layer'. If there are too many to fit in one layer, it splits
// into sublayers
function LayerFill() {
    layerSpacingArr = backendNodeLayerFill([backend], 0)
    sublayersToAddPerLayer = [0]
    for (var layeri = 0; layeri < layerSpacingArr.length; layeri++) {
        sublayersToAddPerLayer.push(layerSpacingArr[layeri].length + sublayersToAddPerLayer[layeri])
    }
    subLayerCount = layerSpacingArr.reduce((acc, obj) => acc + obj.length, 0)
}

// This helper function is from ChatGPT
function argsort(arr) {
    return arr.map((_, i) => i)
              .sort((a, b) => arr[a] - arr[b]);
}

//
function backendNodeLayerFill(backnodes, layer) {

    var nodecount = backnodes.length;
    const nodesize = bnode => bnode.value.length; // lambda to get number of elements
    // Summing the result of applying lambda function to each object (line written with ChatGPT)
    const elcount = backnodes.reduce((acc, obj) => acc + nodesize(obj), 0);
    let minNodeGap = buttonSideLength * 1.5
    var nSublayers = Math.ceil(((elcount * nodeXSidelength) + (nodecount * minNodeGap)) / (canvas.width - minNodeGap))

    let elementspernode = backnodes.map(x => x.value.length)

    var gapsize = []
    var sublayers = []
    var sublayerIndexRef = []
    var sublayersAreResolved = false
    while (!sublayersAreResolved) { // Mathematically SubLayers above should work, but maybe it's hard to split elements evenly
        sublayersAreResolved = true
        gapsize = [];
        var sublayers = Array.from({length: nSublayers}, e => Array(2).fill(0));
        //https://stackoverflow.com/questions/37949813/array-fillarray-creates-copies-by-references-not-by-value
        sublayerIndexRef = Array.from({length: nSublayers}, e => Array())
        //nodeprocessorder = argsort(elementspernode) // Do larger nodes first
        //for (var i = nodeprocessorder.length - 1; i >= 0; i--) {
        var nextsublayer = 0
        for (var i = 0; i < backnodes.length; i++) {
            var iterate = false;
            do {
                iterate = false
                let potentialGap = (canvas.width - ((sublayers[nextsublayer][0] + elementspernode[i]) * nodeXSidelength)) / (sublayers[nextsublayer][1] + 2)
                if (potentialGap < buttonSideLength * 1.5) {
                    nextsublayer++
                    iterate= true
                }
            } while (iterate && nextsublayer < nSublayers);
            if (nextsublayer >= nSublayers) {
                sublayersAreResolved = false
                nSublayers++
                break
            }
            //let nextsublayer = argMin(sublayers)
            backnodes[i].layer = layer
            backnodes[i].sublayer = nextsublayer
            sublayers[nextsublayer][0] += elementspernode[i]
            sublayers[nextsublayer][1] += 1
            sublayerIndexRef[nextsublayer].push(i)
        }
        sublayersAreResolved = true
        // Check all the sublayers have been fitted right
        for (var i = 0; i < sublayers.length; i++) {
            // There should be 1.5 buttons of space in between every node and also between the nodes and edges
            let thisgap = (canvas.width - (sublayers[i][0] * nodeXSidelength)) / (sublayers[i][1] + 1)
            if (thisgap < buttonSideLength * 1.5) {
                nSublayers++;
                sublayersAreResolved = false
                break;
            } else {
                gapsize.push(thisgap)
            }
        }
        // Noone should ever make a tree this big, this will prevent an infinite loop.
        if (sublayers == 20) {
            sublayersAreResolved = true
        }
    }

    for (var subind = 0; subind < sublayerIndexRef.length; subind++) {
        let curSub = sublayerIndexRef[subind];
        curSub.sort(function(a, b) {return a - b;}) // https://stackoverflow.com/questions/1063007/how-to-sort-an-array-of-integers-correctly
        for (var i = 0; i < curSub.length; i++) {
            if (i == 0) {
                backnodes[curSub[i]].xloc = gapsize[subind]
            } else {
                backnodes[curSub[i]].xloc = backnodes[curSub[i - 1]].xloc + (backnodes[curSub[i - 1]].value.length * nodeXSidelength) + gapsize[subind]
            }
        }
    }

    let nextLayerNodes = backnodes.reduce((acc, obj) => acc.concat(obj.children), []); // untested
    if (nextLayerNodes.length == 0) {
        return [gapsize]
    } else {
        backendNodeLayerFill(nextLayerNodes, layer + 1);
        let nextLayerRes = backendNodeLayerFill(nextLayerNodes, layer + 1);
        return [gapsize].concat(nextLayerRes)
    }
}

// This function does the entire movement from backend to frontend trees.
// The previous frontend is removed and replaced every time this is call.
// Handles all button creation and gives locations for every frontend node.
function processBackendJson() {
    if (!backend) {
        return;
    }
    nodes = []
    links = []
    squareButtons = []
    LayerFill()
    root = processBackendJsonNode(backend);
}

function processBackendJsonNode(backnode) {
    let fixlevel = sublayersToAddPerLayer[backnode.layer] + backnode.sublayer

    var ylinklength = 190
    //   Every Link Max length + space at top and bottom + An extra node size
    if ((subLayerCount - 1) * ylinklength + (buttonSideLength*4) + nodeYSidelength > canvas.height) {
        ylinklength = (canvas.height - nodeYSidelength - (buttonSideLength * 4)) / (subLayerCount - 1)
    }
    var newyloc  =  buttonSideLength*2 + (fixlevel * ylinklength);

    var tNode = new Node(backnode.xloc, newyloc);
    if (backnode.highlight) {
        tNode.isAcceptState = true;
    }
    if (backnode.subtree) {
        tNode.isSubTree = true;
    }
    tNode.id = backnode.id;
    tNode.index = backnode.parentIndex
    tNode.text = backnode.value //.map(val => { return String(val)});
    nodes.push(tNode);
    let bottomlevel = (backnode.children.length == 0)
    let canaddnodes = (((backnode.value.length + 2) * nodeXSidelength) < canvas.width) && bottomlevel && canEdit;
    let candeletenodes = bottomlevel && backnode.value.length > 1 && canEdit;
    let canpromote = backnode.value.length > 2 && canEdit;
    let candemote = backnode.children.length > 0 && canEdit;

    tNode.canAddNodes = canaddnodes
    tNode.canDeleteNodes = candeletenodes
    tNode.canPromoteNodes = canpromote
    tNode.canDemoteNodes = candemote
    tNode.wouldDemoteNodes = backnode.children.length > 0

    for (var i = 0; i < backnode.children.length; i++) {
        let child = processBackendJsonNode(backnode.children[i])
        links.push(new Link(tNode, child, true))
    }

    if (canaddnodes) {
        for (var i = 0; i < backnode.value.length; i++) {
            if (i == 0) {
                var tBut = new SquareButton(x=tNode.x,
                    y=tNode.y,
                    id=backnode.id,
                    type="add",
                    isLeft=true,
                    index=i)
                squareButtons.push(tBut);
            }
            var tBut = new SquareButton(x=tNode.x,
                y=tNode.y,
                id=backnode.id,
                type="add",
                isLeft=false,
                index=i)
            squareButtons.push(tBut)


        }
    }
    if (candeletenodes) {
        for (var i = 0; i < backnode.value.length; i++) {
            var tBut = new SquareButton(x=tNode.x, y=tNode.y, id=backnode.id, type="del", isLeft=false, index = i)
            squareButtons.push(tBut);
        }
    }
    if (canpromote) {
        for (var i = 1; i < backnode.value.length - 1; i++) {
            var tBut = new SquareButton(x=tNode.x, y=tNode.y, id=backnode.id, type="pro", isLeft=false, index = i)
            squareButtons.push(tBut);
        }
    }
    if (candemote) {
        for (var i = 0; i < backnode.value.length; i++) {
            var tBut = new SquareButton(x=tNode.x, y=tNode.y, id=backnode.id, type="dem", isLeft=false, index = i)
            squareButtons.push(tBut);
        }
    }

    return tNode;

}

function escapeHtml(unsafe)
{
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

function unescapeHtml(safe)
{
    return safe
         .replace(/&amp;/g, "&")
         .replace(/&lt;/g, "<")
         .replace(/&gt;/g, ">")
         .replace(/&quot;/g, '"')
         .replace(/&#039;/g, "'");
 }
