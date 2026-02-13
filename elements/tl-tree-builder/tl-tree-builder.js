/// TODO TODO Updated Select Bounds

var caretVisible = true; // This alone is declared in global scope, it only gets drawn if a node is selected any way,
var caretTimer;
// and multiple instance should effect it in the same way.

window.TreeBuilderElement = function (name) {
    this.canvas;
    // this.caretTimer;
    this.cursorVisible = true;
    this.movingObject = false;
    this.lastselectedptr = null;
    this.selectedObject = null;
    this.tempObj = null;
    this.originalClick;

    this.snapToPadding = 6; // pixels
    this.hitTargetPadding = 6; // pixels

    // For the backend tree structure in both modes. Equivalent to the python dicts.
    this.backend = null;
    // In pointer mode, ptrretbackend will be submitted instead of backend, which is just for managing the appearance.
    // This allows us to update the backend submission as it's being modified without affecting what the student sees.
    this.ptrretbackend = null;

    // These represent the frontend tree structure in both modes
    this.nodes = [];
    this.root = null;
    this.links = [];

    this.answersName = name;

    this.largeNodeSize = 30;
    this.updateButtonxBound = 200;
    this.updateButtonyBound = 50;
    this.smallNodeSize = 20;
    this.FinalLevelNodesCount = 3;
    this.nodeRadius = this.largeNodeSize;
    this.altNodeRadius = this.smallNodeSize;
    this.buttonSideLength = 13;
    this.nextBacknodeId = 1;
    this.squareButtons = [];
    this.fixHeight = false;
    this.fixHeightDifference = 140; // the initial height difference when fixHeight = true
    this.currentUniversalHeight = this.fixHeightDifference; // used if fixHeight = true
    this.workareawidth = 781
    this.workareaheight = 588

    this.shift = false;
    this.ctrl = false;
    this.editmode;
    this.updatepointererror = "";
    this.ptrretupdateerror = "";
    this.rootptr = "ROOT*"
    this.numeric_input_only = false;
    this.arbitrary_children_mode = false
    this.autonodevals = []
    this.side_tree_start = null;
    this.final_level_val = ""
    this.final_node_count_val = ""
    this.leaf_count_ID = Math.PI;
    this.height_node_ID = Math.E;
    this.enable_final_level = false
    this.enable_height_input = false;
    this.height_node_value = "";
    this.backend_final_level = ""
    this.enable_subtrees = true
    this.expanded_level = -1;
    this.can_expand_level = -1;
    this.sidetreestartloc = this.workareawidth;
    this.height_limit = -1;
    this.treeFrameInd = 0;
    this.TreeFrames = [];
    this.intervalTime = 1000;

    this.node_mode = "circle"
}

window.TreeBuilderElement.prototype.tree_builder_init = function (starterBackend, backendTreeJson, mode, fixNodeYHeight, editable,
    frontdata, numeric_input, side_tree_init, side_tree_start, final_level_section, leaf_value_str, leaf_count_str,
    node_draw_mode, enable_subtrees_, enable_height_input_, height_init, height_limit_, init_small_node, tree_frames,
    interval_time, frontLabelTreeJson){

  // Get canvas from page and initialize context.
    this.canvas = document.getElementById(this.answersName + '-tree-canvas')
    this.workareawidth = this.canvas.width
    this.workareaheight = this.canvas.height
    this.enable_subtrees = (enable_subtrees_ && mode != "recurrence") // Subtrees aren't ready for deploy, just block them for now.
    this.node_mode = node_draw_mode;
    this.enable_height_input = enable_height_input_;
    this.height_node_value = height_init;
    this.height_limit = height_limit_;
    this.side_tree_start = side_tree_start;
    this.intervalTime = interval_time;
    this.treeFrames = tree_frames;
    this.frontLabelTreeJson = frontLabelTreeJson;
    if (fixNodeYHeight || mode == 'recurrence') {
        this.fixHeight = true
        if (mode == 'recurrence') {
            this.fixHeightDifference = 180;
        }
    }
    this.numeric_input_only = numeric_input
    this.enable_final_level = final_level_section
    if (mode == 'recurrence' && this.enable_final_level) {
        this.workareaheight = this.canvas.height - ((2.5)*this.largeNodeSize)-10;
        this.final_level_val = leaf_value_str
        this.final_node_count_val = leaf_count_str
    }
    if (init_small_node) {
        this.nodeRadius = this.smallNodeSize;
        this.altNodeRadius = this.largeNodeSize;
    }

    this.initializeTree(mode, mode == "side-label" ? frontLabelTreeJson : backendTreeJson, frontdata, side_tree_init, this.enable_final_level && (side_tree_init == side_tree_start), enable_height_input_);

    if (mode == 'animation') {
        let advanceAnimation = () => {
            this.treeFrameInd = (this.treeFrameInd + 1) % this.treeFrames.length;
            starterBackend = this.treeFrames[this.treeFrameInd];
            if (this.isPointerMode()) {
                let roottreeJson = '{"value": "';
                let roottreeJson2 = '", "left": ';
                let roottreeJson3 = ',"right": null}';
                let starterWithRoot = roottreeJson.concat(this.rootptr, roottreeJson2, starterBackend, roottreeJson3);
                this.restoreBackendJson(starterWithRoot);
            } else {
                if (starterBackend == null || starterBackend == "") {
                    if (this.arbitrary_children_mode) {
                        starterBackend = '{"value": "","children": []}'
                    } else {
                        starterBackend = '{"value": "","right": null,"left": null}'
                    }

                }
                if (this.editmode == 'recurrence') {
                    this.autonodevals.length = 0
                    this.autonode_init(this.side_tree_start, this.enable_final_level)
                    if (this.enable_height_input) {
                        this.height_node_value = "";
                    }
                    if (this.enable_final_level) {
                        this.final_node_count_val = "";
                    }
                }

                this.restoreBackendJson(starterBackend);
            }
            this.draw();
        }
        setInterval(advanceAnimation, interval_time);
        this.editmode = "view-only"
    }
    if (mode == "side-label") {
        this.sideLabelInit(backendTreeJson, this.backend)
    }

    // If the student is not allowed to edit, we return after drawing.
    if (!editable) {
        return;
    }

    window.addEventListener('click', (e) => {
        if (this.selectedObject != null) {
            this.selectedObject.isSelected = false;
        }
        this.selectedObject = null;
        this.draw();
    }, true)

    this.canvas.addEventListener('click', (e) => {
        // this.resetCaret
        // Get mouse position and select object if possible.
        var mouse = crossBrowserRelativeMousePos(e);
        this.selectedObject = this.selectObject(mouse.x, mouse.y);
        this.movingObject = false;
        this.originalClick = mouse;

        if (this.isPointerMode() && mouse.x < this.updateButtonxBound && mouse.y < this.updateButtonyBound) {
            this.updatePointers()
        }
        if (this.selectedObject != null) {

            if (this.selectedObject instanceof SquareButton) {
                if (this.selectedObject.type == "add") {
                    this.addNewNodeWrapper(this.selectedObject.id, this.selectedObject.isLeft, this.ctrl && this.enable_subtrees);
                    this.ctrl = false;
                } else if (this.selectedObject.type == "del") {
                    if (this.editmode == 'pointer-delete') {
                        this.RemoveFrontendNode(this.selectedObject.id)
                        this.updatePointers(true)
                    } else if (this.editmode == "builder" || this.editmode == "recurrence") {
                        this.RemoveNodeWrapper(this.selectedObject.id);
                    }
                } else if (this.selectedObject.type == "ptr") {
                    if (this.ctrl) {
                        this.removeLink(this.findDrawnNodeById(this.selectedObject.id), this.selectedObject.isLeft);
                        this.lastselectedptr = null;
                        this.updatePointers(true);
                        this.ctrl = false;
                    } else {
                        this.lastselectedptr = this.selectedObject;
                    }
                } else if (this.selectedObject.type == "exp") {
                    this.expandNodeWrapper(this.selectedObject.id, true);
                } else if (this.selectedObject.type == "con") {
                    this.expandNodeWrapper(this.selectedObject.id, false);
                }
            }
            this.resetCaret();
        }

        if (this.selectedObject instanceof Node) {
            if (this.lastselectedptr) {
                this.removeLink(this.findDrawnNodeById(this.lastselectedptr.id), this.lastselectedptr.isLeft)
                this.links.push(new Link(this.findDrawnNodeById(this.lastselectedptr.id), this.selectedObject, this.draw_params, this.lastselectedptr.isLeft));
                this.updatePointers(true)
            }
        }

        this.draw();

        if (!(this.selectedObject instanceof SquareButton && this.selectedObject.type == "ptr")) {
            this.lastselectedptr = null;
        }

        if (canvasHasFocus()) {
            // disable drag-and-drop only if the canvas is already focused
            return false;
        } else {
            // otherwise, let the browser switch the focus away from wherever it was
            this.resetCaret();
            return true;
        }
    }, true);

    this.clearButton = document.getElementById(`${this.answersName}-clear-tree`);
    this.clearButton.addEventListener('click', () => {
        if (window.confirm('Are you sure you want to reset your tree?')) {
            if (this.isPointerMode()) {
                let roottreeJson = '{"value": "';
                let roottreeJson2 = '", "left": ';
                let roottreeJson3 = ',"right": null}';
                let starterWithRoot = roottreeJson.concat(this.rootptr, roottreeJson2, starterBackend, roottreeJson3);
                this.restoreBackendJson(starterWithRoot);
            } else {
                if (starterBackend == null || starterBackend == "") {
                    if (this.arbitrary_children_mode) {
                        starterBackend = '{"value": "","children": []}'
                    } else {
                        starterBackend = '{"value": "","right": null,"left": null}'
                    }

                }
                if (this.editmode == 'recurrence') {
                    this.autonodevals.length = 0
                    this.autonode_init(this.side_tree_start, this.enable_final_level)
                    if (this.enable_height_input) {
                        this.height_node_value = "";
                    }
                    if (this.enable_final_level) {
                        this.final_node_count_val = "";
                    }
                }


                this.restoreBackendJson(this.editmode != "side-label" ? starterBackend : this.frontLabelTreeJson);
                if (this.editmode == "side-label") {
                    this.sideLabelInit(starterBackend, this.backend)
                }
            }
            this.draw();

            if (this.isPointerMode()) {
                this.ptrretbackend = this.backend
                this.updatePointers(true)
            }
        }
    });


    document.getElementById(this.answersName + '-toggle-state-size').addEventListener("click", () => {
        let oldRadius = this.nodeRadius;
        this.nodeRadius = this.altNodeRadius;
        this.altNodeRadius = oldRadius;
        this.draw_params.nodeRadius = this.nodeRadius;
        this.updateAllDrawParams();
        this.toggleButtonsForRadius();
        this.draw();
    })

    document.getElementById(this.answersName + '-toggle-mode').addEventListener('click', () => {
        if (!(this.editmode == "builder" || this.editmode == "pointer")) {
            return;
        }
        if (this.editmode == 'pointer') {
            this.updatePointers(true)
        }
        // Effectively tries to output the tree and then reinitializes it as if the tree was just generating.
        let tempjsondata = this.getReturnJsonData()
        if (this.editmode == 'pointer' && this.ptrretupdateerror != "") {
            this.updatePointers()
            this.draw()
            return;
        }
        this.initializeTree(this.editmode == 'pointer' ? 'builder': 'pointer', tempjsondata[1], tempjsondata[2], tempjsondata[3])
    });

    document.addEventListener('keydown', (e) => {
        var key = crossBrowserKey(e);

        if (!canvasHasFocus()) {
            // don't read keystrokes when other things have focus
            return true;
        } else if (key == 17) { // ctrl key
            this.ctrl = true;
        } else if (key == 8) { // backspace key
            if (this.isPointerMode() || this.editmode == "view-only") {
                return false
            }
            if (this.selectedObject != null && 'text' in this.selectedObject) {
                this.selectedObject.text = this.selectedObject.text.substr(0, this.selectedObject.text.length - 1);
                this.resetCaret();
                this.draw();
            }

            // backspace is a shortcut for the back button, but do NOT want to change pages
            return false;
        }

    });

    document.addEventListener('keypress', (e) => {
        // don't read keystrokes when other things have focus
        var key = crossBrowserKey(e);
        keyBounds = false

        if (this.selectedObject instanceof Node || this.selectedObject instanceof Link && this.selectedObject.editable) {
            if (this.numeric_input_only) {
                keyBounds = (key >= 48 && key <= 57) || (key== 45 || key == 109 || key == 173 || key == 189) //Different options for '-'
            } else {
                keyBounds = (key >= 0x20 && key <= 0x7E)
            }
        }
        if (!canvasHasFocus()) {
            // don't read keystrokes when other things have focus
            return true;

        } else if (!this.isPointerMode() && this.editmode != "view-only" && keyBounds && !e.metaKey && !e.altKey && !e.ctrlKey && this.selectedObject != null && 'text' in this.selectedObject) {
            // Reset highlighting when user types

            this.selectedObject.text += String.fromCharCode(key);
            this.resetCaret();
            this.draw();

            // don't let keys do their actions (like space scrolls down the page)
            return false;
        } else if (key == 8) {
            // backspace is a shortcut for the back button, but do NOT want to change pages
            return false;
        }
    });

    document.addEventListener('keyup', (e) => {
        var key = crossBrowserKey(e);

        if (key == 17) { // ctrl key
            this.ctrl = false;
        }
    });
}

window.TreeBuilderElement.prototype.isPointerMode =  function () {
    return (this.editmode == 'pointer' || this.editmode == 'pointer-delete')
}

// If we're going off of starter side tree json, it doesn't include the final level. If the code has already been submited once,
// it does. add_side_final_level handles this.
window.TreeBuilderElement.prototype.initializeTree = function (mode, backendTreeJson, frontdata, sideTreeData, add_side_final_level=false, enable_height=false) {
    this.ptrretupdateerror = ""
    this.updatepointererror = ""

    if (mode == "pointer") {
        this.editmode = mode;
    } else if (mode == "pointer-delete") {
        this.editmode = mode;
    } else if (mode == "recurrence") {
        this.editmode = mode
        this.arbitrary_children_mode = true
        this.workareawidth = this.canvas.width - (this.nodeRadius*2) - (this.buttonSideLength*2) - (enable_height ? (this.largeNodeSize / 2) : 0);
        this.sidetreestartloc = enable_height ? this.workareawidth + this.largeNodeSize : this.workareawidth;
        this.autonode_init(sideTreeData, add_side_final_level)
    } else if (mode == "value") {
        this.editmode = "value"
    } else if (mode == "view-only" || mode == "animation") {
        this.editmode = "view-only"
    } else if (mode == "side-label") {
        this.editmode = "side-label";
        this.workareawidth = this.canvas.width - (this.largeNodeSize * 1.5)
    } else {
        this.editmode = "builder";
    }

    this.draw_params = {
        nodeRadius: this.nodeRadius,
        buttonSideLength: this.buttonSideLength,
        rootptr: this.rootptr,
        editmode: this.editmode,
        draw_caret: !this.isPointerMode() && this.editmode != "view-only"
    }

    if (backendTreeJson == null || backendTreeJson == "") {

        if (this.arbitrary_children_mode) {
            backendTreeJson = '{"value": "","children": []}'
        } else {
            backendTreeJson = '{"value": "","right": null,"left": null}';
        }

    }
    if (this.isPointerMode()) {
        let roottreeJson = '{"value": "';
        let roottreeJson2 = '", "left": ';
        let roottreeJson3 = ',"right": null}';
        backendTreeJson = roottreeJson.concat(this.rootptr, roottreeJson2, backendTreeJson, roottreeJson3);
    }
    this.restoreBackendJson(backendTreeJson);
    this.draw();
    if (this.isPointerMode()) {
        this.ptrretbackend = this.backend
        this.updatePointers(true)
        if (frontdata) {
            this.restoreFrontendJson(frontdata);
        }
    }
}

window.TreeBuilderElement.prototype.sideLabelInit = function (sideLabelsJson, backend) {
    sideLabelTree = reformatJson(sideLabelsJson);
    this.backend = mergeTreesNode(backend, sideLabelTree);
    this.processBackendJson();
    this.draw();
}

function mergeTreesNode(frontTree, valueTree) {
    if (frontTree == null) {
        return null;
    }
    frontTree.frontLabel = frontTree.value
    frontTree.value = valueTree != null ? valueTree.value : ""
    frontTree.left = mergeTreesNode(frontTree.left, valueTree != null ? valueTree.left : null)
    frontTree.right = mergeTreesNode(frontTree.right, valueTree != null ? valueTree.right : null)
    return frontTree
}

window.TreeBuilderElement.prototype.autonode_init = function (sidejson, final_level_element=false) {
    var beclean = sidejson.replace(/'/g, '"');
    var beclean2 = beclean.replace(/None/g, "null");
    var beclean3 = beclean2.replace(/False/g, 'false');
    var beclean4 = beclean3.replace(/True/g, 'true');
    this.autonodevals = JSON.parse(beclean4)
    this.autonodevals.forEach(unescapeHtml)
    // There's some weird quirks in how autonodevals gets updated that means the code just always assumes
    // the array is one longer than it needs to be.
    if (this.autonodevals.length > 0 && this.autonodevals[this.autonodevals.length - 1] != '') {
        this.autonodevals.push('')
    }
    if (final_level_element) {
        this.autonodevals.unshift('')
    }
}

window.TreeBuilderElement.prototype.updateAllDrawParams = function () {
    for (let i = 0; i < this.squareButtons.length; i++) {
        this.squareButtons[i].p = this.draw_params;
    }
    for (let i = 0; i < this.nodes.length; i++) {
        this.nodes[i].p = this.draw_params;
    }
    for (let i = 0; i < this.links.length; i++) {
        this.links[i].p = this.draw_params;
    }
}

window.TreeBuilderElement.prototype.toggleButtonsForRadius = function () {
    for (let i = 0; i < this.squareButtons.length; i++) {
        this.squareButtons[i].toggleloc();
    }
}

window.TreeBuilderElement.prototype.findDrawnNodeById = function (id) {
    for (var i = 0; i < this.nodes.length; i++) {
        if (this.nodes[i].id == id) {
            return this.nodes[i];
        }
    }
}

// Takes the id of a child, Searches the links for the child, returns the parent node from that link
window.TreeBuilderElement.prototype.getFrontendParent = function (childId) {
    for (let i = 0; i < this.links.length; i++) {
        if (this.links[i].nodeB.id == childId) {
            return this.links[i].nodeA;
        }
    }
    return null
}

// Takes in the backend root and the ID of the child node, returns ID of parent
function getBackendParentID(backnode, childId) {
    // sneaky way to check for arbitrary children mode, this means it doesn't have to be a class function
    if (backnode.children === undefined || backnode.children === null) {
        throw new Error("The function getBackendParentID has not yet been implemented for binary trees.")
    }
    if (backnode.children.length == 0) {
        return -1;
    }
    for (let i = 0; i < backnode.children.length; i++) {
        if (backnode.children[i].id == childId) {
            return backnode.id;
        } else {
            let ret = getBackendParentID(backnode.children[i], childId)
            if (ret != -1) {
                return ret;
            }
        }
    }
    return -1;
}

// Removes the link from parent to this node
window.TreeBuilderElement.prototype.removeLink = function(node, isLeftSource) {
    for (var i = 0; i < this.links.length; i++){
        if (this.links[i].nodeA.id == node.id && this.links[i].isLeftLink == isLeftSource) {
            this.links.splice(i, 1);
            return;
        }
    }
    this.draw();
}

// Removes all links to or from the node with this id
window.TreeBuilderElement.prototype.removeAllLinks = function(removeId) {
    for (var i = 0; i < this.links.length; i++){
        if (this.links[i].nodeA.id == removeId || this.links[i].nodeB.id == removeId) {
            this.links.splice(i, 1);
            i--;
        }
    }
    this.draw();
}

// Removes all links to or from the node with this id
window.TreeBuilderElement.prototype.removeAllSquareButtons = function(removeId) {
    for (var i = 0; i < this.squareButtons.length; i++){
        if (this.squareButtons[i].id == removeId) {
            this.squareButtons.splice(i, 1);
            i--;
        }
    }
    this.draw();
}

// ptrret is what is returned on save&grade, the default is what the student will see.
window.TreeBuilderElement.prototype.updatePointers = function (ptrret=false) {
    let newpointererror = ""

    let represented_node_ids = [];
    // Go through every edge and check nodeB (the child node) and make sure no node is a child from multiple parents
    for (var i = 0; i < this.links.length; i++){
        let considernode = this.links[i].nodeB;
        if (represented_node_ids.indexOf(considernode.id) > -1) {
            let fronterr = "Error: multiple pointers pointing to node with value ";
            newpointererror = fronterr.concat(considernode.text)
            break;
        } else {
            represented_node_ids.push(considernode.id);
        }
    }
    // Make sure every node is either the root, or being pointed to by an edge.
    for (var i = 0; i < this.nodes.length && newpointererror == ""; i++) {
        if (represented_node_ids.indexOf(this.nodes[i].id) == -1 && this.nodes[i].text != this.rootptr) {
            let fronterr = "Error: no pointers pointing to node with value ";
            newpointererror = fronterr.concat(this.nodes[i].text)
            break;
        }
    }
    // If this is a submission -> if it's invalid, we revert to the most recent valid state for submission.
    // The error message will be pushed up to the student
    if (ptrret) {
        this.ptrretupdateerror = newpointererror
        if (newpointererror != "") {
            this.saveBackup()
            return;
        }
        this.ptrupdaterec(this.ptrretbackend)
        this.saveBackup()
    // If we're not submitting and it's invalid the new error will get shown on the board (from code elsewhere) and we won't change the tree
    // If it's valid, make the backend match the new front end and redraw the tree.
    } else {
        this.updatepointererror = newpointererror
        if (newpointererror != "") { return;}
        this.ptrupdaterec(this.backend)
        this.processBackendJson()
    }
}

window.TreeBuilderElement.prototype.ptrupdaterec = function(backnode) {
    backnode.left = null;
    backnode.right = null;
    // For every link, see if it comes from this node. If so, add children, and
    // recursively try to add that nodes children. If we've filled both children, we can exit the loop early.
    for (var i = 0; i < this.links.length; i++){
        if (this.links[i].nodeA.id == backnode.id) {
            this.addNewNode(backnode, this.links[i].nodeA.id, this.links[i].isLeftLink,
                this.links[i].nodeB.isSubTree, this.links[i].nodeB.isAcceptState, this.links[i].nodeB.id, this.links[i].nodeB.text)

            if (this.links[i].isLeftLink) {
                this.ptrupdaterec(backnode.left)
            } else {
                this.ptrupdaterec(backnode.right)
            }
            // If both of the current node's children have been filled, we can stop looking through all the links
            if (backnode.right != null && backnode.left != null) {
                return;
            }
        }
    }
}

window.TreeBuilderElement.prototype.draw = function() {
    this.drawUsing(this.canvas.getContext('2d'));
    this.saveBackup();
}

window.TreeBuilderElement.prototype.drawUsing = function(c) {
    c.clearRect(0, 0, this.canvas.width, this.canvas.height);
    c.save();
    // c.translate(0.5, 0.5);

    if (this.isPointerMode()) {
        c.font = "26px Courier New"
        c.lineWidth = 1;
        var color = 'black'
        c.fillStyle = c.strokeStyle = color
        c.beginPath();
        c.rect(0, 0, this.updateButtonxBound, this.updateButtonyBound);
        c.stroke()
        c.fillText("Re-Draw Tree", 3, this.updateButtonyBound / 2, this.updateButtonxBound - 6)

        if (this.updatepointererror != "") {

            c.fillText(this.updatepointererror, this.workareawidth / 2 + (this.nodeRadius * 1.2), this.updateButtonyBound / 2, (this.workareawidth / 2 - this.nodeRadius* 1.5))
        }
    }
    if (this.editmode == 'recurrence') {
        var color = 'black'
        c.fillStyle = c.strokeStyle = color
        c.font = "20px Courier New"

        if (this.enable_height_input) {
            c.lineWidth = 1;
            c.fillText("Height", this.workareawidth - this.largeNodeSize, this.canvas.height / 2 - this.largeNodeSize - this.buttonSideLength / 2, 2 * this.largeNodeSize);
        } else {
            c.lineWidth = 2;
            c.moveTo(this.workareawidth, 0);
            c.lineTo(this.workareawidth, this.canvas.height);
            c.stroke();
        }

        if (this.enable_final_level) {
            c.lineWidth = 1;
            c.fillText("Total # Leaves:", this.workareawidth - this.largeNodeSize*7, (this.workareaheight + this.canvas.height) / 2, this.largeNodeSize * 4.5)
        }

        c.lineWidth = 1
        c.fillText("Work Per", this.workareawidth + 3, 15, this.canvas.width)
        c.fillText("Level", this.workareawidth + 3, 35, this.canvas.width)
        c.fillText("Work Per Call", (this.workareawidth / 2) - (this.largeNodeSize*2), 25, this.largeNodeSize*4)
    }

    for (var i = 0; i < this.links.length; i++){
        c.lineWidth = 1;
        var color = 'black'
        c.fillStyle = c.strokeStyle = color
        this.links[i].draw(c);
    }

    for (var i = 0; i < this.nodes.length; i++){
        c.lineWidth = 1;
        var color = 'black'
        if (this.nodes[i] == this.selectedObject) {
            color = 'blue'
        }
        c.fillStyle = c.strokeStyle = color
        this.nodes[i].draw(c);
    }

    for (var i = 0; i < this.squareButtons.length; i++) {
        c.lineWidth = 1;
        this.squareButtons[i].draw(c);
    }

    if (this.tempObj){
        c.lineWidth = 1;
        c.fillStyle = c.strokeStyle = 'black'
        this.tempObj.draw(c);
    }
}


window.TreeBuilderElement.prototype.selectObject = function(x, y) {
    if (this.selectedObject != null) {
        this.selectedObject.isSelected = false;
    }

    for (var i = 0; i < this.squareButtons.length; i++) {
        if (this.squareButtons[i].containsPoint(x, y)) {
            this.squareButtons[i].isSelected = true;
            return this.squareButtons[i];
        }
    }

    for (var i = 0; i < this.nodes.length; i++) {
        if (this.nodes[i].containsPoint(x, y) && !this.nodes[i].decoration) {
            this.nodes[i].isSelected = true;
            return this.nodes[i];
        }
    }

    return null;
}

function canvasHasFocus() {
    return (document.activeElement || document.body) == document.body;
}

window.TreeBuilderElement.prototype.resetCaret = function() {
    clearInterval(caretTimer);
    caretTimer = setInterval(() => {caretVisible = !caretVisible; this.draw();}, 500);// draw()', 500);
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

window.TreeBuilderElement.prototype.saveBackup = function() {
    if (!JSON){
        return;
    }

    $('input#' + this.answersName + '-raw-json').val(this.getReturnJsonData()[0])
}

window.TreeBuilderElement.prototype.getReturnJsonData = function () {
    var parentTemp = [];
    this.updateBackendText()
    escapeNode(this.backend)
    this.autonodevals.forEach(escapeHtml)

    var submit = this.backend
    if (this.isPointerMode()) {
        submit = this.ptrretbackend ? this.ptrretbackend.left : null
    }

    var backup = {
        'backendRoot': submit,
        // currentMode is so when a student toggles the state and then submits it will stay in the most recent mode the student was in
        'currentMode': this.editmode,
        // 'frontend' is so pointer mode can restore an illegal state the student is currently editing
        'frontend': {'nodes': this.nodes, 'links': this.links, 'squarebuttons': this.squareButtons, 'redraw_required': (this.ptrretupdateerror != "")},
        'format-errors': this.ptrretupdateerror,
        'sideTree': this.autonodevals,
        'leaf-count': this.final_node_count_val,
        'height-val': this.height_node_value
        }

    toreturn = [JSON.stringify(backup), JSON.stringify(submit), JSON.stringify(backup.frontend), JSON.stringify(this.autonodevals)]
    return toreturn
}

window.TreeBuilderElement.prototype.updateBackendText = function() {
    if (this.editmode == 'recurrence') {
        let h = arbChildBackendNodeHeight(this.backend)
        this.autonodevals = new Array(h).fill("")
        for (let i = 0; i < h+1 + (this.enable_final_level ? 1 : 0); i++) {
            let node = this.findDrawnNodeById(-1 * (i+1))
            this.autonodevals[i] = node == null ? "" : node.text
        }

        if (this.enable_final_level) {
            this.final_node_count_val = this.findDrawnNodeById(this.leaf_count_ID).text;
        }

        if (this.enable_height_input) {
            this.height_node_value = this.findDrawnNodeById(this.height_node_ID).text;
        }
    }
    this.updateBackendTextNode(this.backend);
}

window.TreeBuilderElement.prototype.updateBackendTextNode = function (backnode) {
    if (backnode == null) {
        return;
    }
    var drawnNode = this.findDrawnNodeById(backnode.id);
    if (drawnNode == null) {
        return;
    }
    backnode.value = drawnNode.text;
    if (this.arbitrary_children_mode) {
        backnode.children.forEach((e) => this.updateBackendTextNode(e))
    } else {
        this.updateBackendTextNode(backnode.left);
        this.updateBackendTextNode(backnode.right);
    }
}

// Only used in the case when we're using pointer mode and the student submits code in an error state
// so it needs to be redrawn in a way that backend json can't represent
window.TreeBuilderElement.prototype.restoreFrontendJson = function (frontdata) {
    var beclean = frontdata.replace(/'/g, '"');
    var beclean2 = beclean.replace(/None/g, "null");
    var beclean3 = beclean2.replace(/False/g, 'false');
    var beclean4 = beclean3.replace(/True/g, 'true');
    let fdata = JSON.parse(beclean4)
    // barrier to prevent unnecessary processing as right now the only case this is needed
    // is if the student submits a tree in an error state
    if (fdata.redraw_required) {
        this.nodes = []
        this.links = []
        this.squareButtons = []

        let fnodes = fdata.nodes
        for (var i = 0; i < fnodes.length; i++) {
            let fnode = fnodes[i]
            var node = new Node(fnode.x, fnode.y, this.draw_params);
            node.isAcceptState = fnode.isAcceptState;
            node.text = unescapeHtml(fnode.text);
            node.mouseOffsetX = fnode.mouseOffsetX;
            node.mouseOffsetY = fnode.mouseOffsetY;
            node.id = fnode.id;
            node.isSubTree = fnode.isSubTree;
            this.nodes.push(node);
        }
        let flinks = fdata.links
        for (var i = 0; i < flinks.length; i++) {
            let flink = flinks[i]
            var link = new Link(this.findDrawnNodeById(flink.nodeA.id), this.findDrawnNodeById(flink.nodeB.id), this.draw_params);
            link.parallelPart = flink.parallelPart;
            link.perpendicularPart = flink.perpendicularPart;
            link.isLeftLink = flink.isLeftLink;
            this.links.push(link);
        }
        let fsbs = fdata.squarebuttons
        for (var i = 0; i < fsbs.length; i++) {
            let fsb = fsbs[i]
            var sb = new SquareButton(fsb.x, fsb.y, fsb.id, fsb.type, fsb.isLeft, this.draw_params, fsb.altx, fsb.alty)
            this.squareButtons.push(sb)
        }

        // The updatePointers call is to redisplay the error message
        this.updatePointers()
        this.draw()
    }
}

function reformatJson (backendJson) {
    var beclean = backendJson.replace(/'/g, '"');
    var beclean2 = beclean.replace(/None/g, "null");
    var beclean3 = beclean2.replace(/False/g, 'false');
    var beclean4 = beclean3.replace(/True/g, 'true');
    var treenodes = JSON.parse(beclean4)
    unescapeNode(treenodes)
    return treenodes
}

window.TreeBuilderElement.prototype.restoreBackendJson = function(backendJson) {
    if (!backendJson) {
        this.backend = null;
    }
    try {
        this.backend = reformatJson(backendJson);
    } catch (e) {
        console.log(e)
        return;
    }
    this.populateBackendIds(this.backend);
    this.processBackendJson();
}

window.TreeBuilderElement.prototype.populateBackendIds = function(bnode) {
    if (bnode) {
        // Pointer mode is dependent on the rootptr's id never changing, we fix it here.
        if (this.isPointerMode() && bnode.value == this.rootptr) {
            bnode.id = 0
        } else {
            bnode.id = this.nextBacknodeId;
            this.nextBacknodeId++;
        }

        if (this.arbitrary_children_mode) {
            bnode.children.forEach((e) => this.populateBackendIds(e));
        } else {
            this.populateBackendIds(bnode.left);
            this.populateBackendIds(bnode.right);
        }
    }
}

function backendNodeDatafill(benode) {
    //Having return values seems redundant but prevents the need for repetitive null-checking
    if (!benode) {
        return [0,0,0];
    }

    let leftvals = backendNodeDatafill(benode.left);
    let rightvals = backendNodeDatafill(benode.right);
    var leftHeight = leftvals[0]
    var rightHeight = rightvals[0]
    benode.leftChildren = 1 + leftvals[1] + leftvals[2]
    benode.rightChildren = 1 + rightvals[1] + rightvals[2]
    if (leftHeight >= rightHeight) {
        benode.height = 1 + leftHeight
        return [benode.height, benode.leftChildren, benode.rightChildren];
    } else {
        benode.height = 1 + rightHeight
        return [benode.height, benode.leftChildren, benode.rightChildren];
    }
}

// Only use on arbitrary child mode
function arbChildBackendNodeHeight(backnode) {
    return (backnode.subsubtree ? 0 : 1) + Math.max(0, ...backnode.children.map(arbChildBackendNodeHeight))
}

function backendNodesAtLevel(backnode, level) {
    if (backnode.level == level) {
        if (backnode.subsubtree) {return 0;}
        return 1;
    }
    return backnode.children.reduce((acc, e) => acc + backendNodesAtLevel(e, level), 0);
}

function backendNodeLevelFill(backnode, level=1) {
    backnode.level = level
    if (backnode.expanded) {
        expanded_level = level
    }
    backnode.children.forEach((e) => backendNodeLevelFill(e, level + 1));
}

// If expand is false, contracts node instead
window.TreeBuilderElement.prototype.expandNodeWrapper = function(id, expand=true) {
    expandNode(this.backend, id, expand);
    this.updateBackendText();
    this.processBackendJson();
    this.draw();
}

function expandNode(backnode, id, expand) {
    if (backnode.id == id) {
        backnode.expanded = expand;
        return true;
    } else {
        return backnode.children.some((e) => {return expandNode(e, id, expand)});
    }
}

window.TreeBuilderElement.prototype.addNewNodeWrapper = function(newNodeId, newNodeIsLeft, subtree) {
    this.updateBackendText();
    this.addNewNode(this.backend, newNodeId, newNodeIsLeft, subtree);
    this.processBackendJson();
    this.draw();
}

window.TreeBuilderElement.prototype.addNewNode =
    function (backnode, newParentNodeId, newNodeIsLeft, subtree, highlight=false, newChildId=null, newChildValue = "", subsubtree=false) {

    if (!backnode) {
        return false;
    }
    if (this.arbitrary_children_mode) {
        if (backnode.id == newParentNodeId) {
            if (backnode.children.length > 0) {
                subtree = false;
            }

            var newNode = {value: newChildValue,
                children: [],
                id: ((newChildId != null) ? newChildId : this.nextBacknodeId),
                subtree: subtree,
                subsubtree: subsubtree,
                highlight: highlight};

            this.nextBacknodeId++;
            backnode.children.push(newNode)
            if (this.editmode == "recurrence" && subtree) {
                this.addNewNode(newNode, newNode.id, newNodeIsLeft, false, false, null, "", true);
            }
            return true;
        } else {
            const recursivecall = (child) => {this.addNewNode(child, newParentNodeId, newNodeIsLeft, subtree, highlight, newChildId, newChildValue, subsubtree)}
            return backnode.children.some(recursivecall)
        }
    } else {
        if (backnode.id == newParentNodeId) {

            var newNode = {value: newChildValue,
                left: null, right: null,
                id: ((newChildId != null) ? newChildId : this.nextBacknodeId),
                subtree: subtree,
                highlight: highlight};

            this.nextBacknodeId++;
            if (newNodeIsLeft) {
                backnode.left = newNode;
            } else {
                backnode.right = newNode;
            }
            return true;
        } else {
            return (this.addNewNode(backnode.left, newParentNodeId, newNodeIsLeft, subtree, highlight, newChildId, newChildValue) || this.addNewNode(backnode.right, newParentNodeId, newNodeIsLeft, subtree, highlight, newChildId, newChildValue));
        }
    }
}

window.TreeBuilderElement.prototype.RemoveFrontendNode = function(removeNodeId) {
    this.removeAllLinks(removeNodeId)
    this.removeAllSquareButtons(removeNodeId)
    for (var i = 0; i < this.nodes.length; i++) {
        if (this.nodes[i].id == removeNodeId) {
            this.nodes.splice(i, 1);
        }
    }
    this.draw();
}

window.TreeBuilderElement.prototype.RemoveNodeWrapper = function(removeNodeId) {
    this.updateBackendText();
    this.RemoveNode(this.backend, removeNodeId);
    this.processBackendJson();
    this.draw();
}

window.TreeBuilderElement.prototype.RemoveNode = function(backnode, removeNodeId) {
    if (!backnode) {
        return false;
    }
    if (this.arbitrary_children_mode) {
        for (let i = 0; i < backnode.children.length; i++) {
            if (backnode.children[i].id == removeNodeId) {
                backnode.children.splice(i, 1)
                return true;
            }
        }
        const recursivecall = (child) => {this.RemoveNode(child, removeNodeId)}
        return backnode.children.some(recursivecall)
    } else {
        if (backnode.left != null && backnode.left.id == removeNodeId) {
            backnode.left = null;
            return true;
        } else if (backnode.right != null && backnode.right.id == removeNodeId) {
            backnode.right = null;
            return true;
        }
        return (this.RemoveNode(backnode.left, removeNodeId) || this.RemoveNode(backnode.right, removeNodeId));
    }
}

window.TreeBuilderElement.prototype.processBackendJson = function() {
    if (!this.backend) {
        return;
    }
    this.nodes = []
    this.links = []
    this.squareButtons = []
    let startheight = (this.editmode == 'recurrence') ? 70 : 35
    if (this.editmode == "side-label") {
        startheight += this.largeNodeSize * 0.6
    }
    if (this.arbitrary_children_mode) {
        this.backend.height = arbChildBackendNodeHeight(this.backend)
    } else {
        backendNodeDatafill(this.backend)
    }
    if (this.fixHeight) {
        this.currentUniversalHeight = Math.min(this.fixHeightDifference, (this.workareaheight - (this.nodeRadius + startheight)) / (this.backend.height))
    }

    if (this.editmode == 'recurrence') {
        for (let i = 0; i < this.backend.height + (this.enable_final_level ? 1 : 0); i++) {

            sidenode = new Node((this.sidetreestartloc + this.canvas.width) / 2,
                    this.enable_final_level && i == 0 ? (this.workareaheight + this.canvas.height) / 2 :
                    (startheight + ((i - (this.enable_final_level ? 1 : 0)) * this.currentUniversalHeight)), this.draw_params);
            sidenode.id = -1 * (i + 1);
            sidenode.text = i + 1 < this.autonodevals.length ? this.autonodevals[i] : "";
            sidenode.square = true;
            this.nodes.push(sidenode);
        }
        expanded_level = -1;
        backendNodeLevelFill(this.backend);
        if (this.enable_final_level) {
            let center_bottom = (this.workareaheight + this.canvas.height) / 2
            let finalx = 0;
            for (let i = 0; i < this.FinalLevelNodesCount; i++) {
                let node = new Node(this.nodeRadius * (1 + i*2), center_bottom, this.draw_params);
                node.text = this.final_level_val;
                node.decoration = true;
                this.nodes.push(node);
                finalx = node.x;
            }
            this.genEllipsis(finalx + this.nodeRadius + 5, center_bottom + this.nodeRadius / 2, this.workareawidth - 6.25*this.largeNodeSize, center_bottom + this.nodeRadius / 2, null, 15);
            lcnode = new Node(this.workareawidth - 1.5*this.largeNodeSize, center_bottom, this.draw_params);
            lcnode.square = true;
            lcnode.id = this.leaf_count_ID;
            lcnode.text = this.final_node_count_val;
            this.nodes.push(lcnode)
        }
    }
    if (this.enable_height_input) {
        hnode = new Node(this.workareawidth, this.canvas.height / 2, this.draw_params);
        hnode.square = true;
        hnode.text = this.height_node_value;
        hnode.id = this.height_node_ID;
        this.nodes.push(hnode);
        this.links.push(new Link(hnode, PointNode(this.workareawidth, this.canvas.height, this.draw_params), this.draw_params))
        this.links.push(new Link(PointNode(this.workareawidth, hnode.y - this.nodeRadius, this.draw_params), PointNode(this.workareawidth, 0, this.draw_params), this.draw_params))
    }

    root = this.processBackendJsonNode(this.backend, 20, this.workareawidth - 20, startheight, this.workareaheight - 40, true);

    if (this.enable_final_level) {
        lowy = this.nodes.reduce((a,b) => Math.max(a, (b.y > this.workareaheight || b.square) ? 0 : b.y), 0);
        //Assume nodes below the work area are in the final level zone.
        this.genEllipsis(this.workareawidth / 2, lowy + this.nodeRadius*1.5, this.workareawidth / 2, this.workareaheight, null, minDots=8);
    }
}

// OO edit
window.TreeBuilderElement.prototype.processBackendJsonNode = function(backnode, xleft, xright, ytop, ybottom, isRoot) {
    let circlediff = (2 ** -0.5) * this.nodeRadius
    let altcirclediff = (2 ** -0.5) * this.altNodeRadius

    let newyloc  = ytop + ((ybottom - ytop) / backnode.height);

    // Set a limit on edge lengths so that don't immediately go to the bottom of the screen, allows more space
    if (newyloc > ytop + 190) {
        newyloc = ytop + 190;
    }
    if (this.fixHeight) {
        newyloc = ytop + this.currentUniversalHeight;
    }
    if (this.editmode == 'recurrence' && backnode.subsubtree) {
        newyloc = ytop + 2*this.nodeRadius;
    }

    // This should move the node further to the right if there are more nodes on the left and vice versa
    // really just a weighted average
    let newxloc =  this.arbitrary_children_mode ? ((xright + xleft) / 2) : (((xleft * backnode.rightChildren) + (xright * backnode.leftChildren)) / (backnode.leftChildren + backnode.rightChildren))
    var tNode = new Node(newxloc, newyloc, this.draw_params);
    if (backnode.highlight) {
        tNode.isAcceptState = true;
    }
    if (backnode.subtree) {
        tNode.isSubTree = true;
    }
    if (backnode.subsubtree) {
        tNode.isSubSubTree = true;
    }
    tNode.id = backnode.id;
    if (isRoot) {
        tNode.y = ytop
        if (this.isPointerMode()) {
            tNode.x = this.workareawidth / 2
        }
    }
    tNode.text = String(backnode.value);
    this.nodes.push(tNode);
    let canaddnodes = (!backnode.subtree) && (!backnode.subsubtree) && (this.editmode == "builder" || (this.editmode == "recurrence" && !(backnode.children.length > 0 && backnode.children[0].subtree) && backnode.level != this.expanded_level - 1 && !(this.height_limit > 0 && backnode.level >= this.height_limit)));
    let candeletenodes = !isRoot && ((this.editmode == "recurrence" && (backnode.children.length == 0 || backnode.subtree) && !backnode.subsubtree) || ((this.editmode == "builder") && !backnode.right && !backnode.left) || (this.editmode == "pointer-delete"));

    if (this.arbitrary_children_mode) {
        if (canaddnodes) {
            var tBut = new SquareButton(x=tNode.x,
                y=tNode.y + circlediff,
                id=backnode.id,
                type="add",
                isLeft=true,
                params=this.draw_params,
                altx=tNode.x,
                alty=tNode.y + altcirclediff)
            this.squareButtons.push(tBut);
        }
        let space = (xright - xleft) / backnode.children.length
        for (let i = 0; i < backnode.children.length; i++) {
            child = backnode.children[i]
            frontendChild = this.processBackendJsonNode(child, xleft + (space * i), xleft + (space * (i+1)), tNode.y, ybottom, false);


            if (!backnode.subtree) {
                this.links.push(new Link(tNode, frontendChild, this.draw_params, false));
            } else {
                let leftbound = backnode.expanded ? 0 : xleft;
                let rightbound = backnode.expanded ? this.workareawidth : xright;
                let ybound = tNode.y;
                let source = tNode;
                if (rightbound - leftbound > 2.5*this.largeNodeSize) {
                    this.links.push(new Link(source, PointNode(leftbound, ybound, this.draw_params), this.draw_params, false));
                    this.links.push(new Link(source, PointNode(rightbound, ybound, this.draw_params), this.draw_params, false));
                }

                this.genEllipsis(leftbound, ybound -6, rightbound, ybound -6);

                // The link from parent to child hasn't been created yet, so we have to go through the backend to find it's id.
                let parent = this.findDrawnNodeById(getBackendParentID(this.backend, tNode.id));
                if (xright - xleft > 2.5*this.largeNodeSize) {
                    this.links.push(new Link(parent, PointNode((tNode.x + 2*xleft) / 3, (tNode.y - (this.nodeRadius / 2)), this.draw_params), this.draw_params))
                    this.links.push(new Link(parent, PointNode((tNode.x + 2*xright) / 3, (tNode.y - (this.nodeRadius / 2)), this.draw_params), this.draw_params))
                }


                if (!backnode.expanded && backendNodesAtLevel(this.backend, backnode.level) == 1) {
                    var tBut = new SquareButton(x = tNode.x - circlediff, y= tNode.y - circlediff - 2*this.buttonSideLength, id = backnode.id, type="exp",
                        isLeft = false, params=this.draw_params, altx = tNode.x - altcirclediff, alty= tNode.y - altcirclediff - 2*this.buttonSideLength);
                    this.squareButtons.push(tBut);
                } else if (backnode.expanded) {
                    var tBut = new SquareButton(x = tNode.x - circlediff, y= tNode.y - circlediff - 2*this.buttonSideLength, id = backnode.id, type="con",
                        isLeft = false, params=this.draw_params, altx = tNode.x - altcirclediff, alty= tNode.y - altcirclediff - 2*this.buttonSideLength);
                    this.squareButtons.push(tBut);
                }
            }
        }
        if (candeletenodes) {
            var tBut = new SquareButton(x=tNode.x + circlediff, y=tNode.y - circlediff - this.buttonSideLength,
                id=backnode.id, type="del", isLeft=false, params=this.draw_params, altx=tNode.x + altcirclediff, alty=tNode.y - altcirclediff - this.buttonSideLength)

            this.squareButtons.push(tBut);
        }
    } else {
        if (backnode.left != null) {
            var nodeLeft;
            if (isRoot && this.isPointerMode()) {
                nodeLeft = this.processBackendJsonNode(backnode.left, 20, this.workareawidth - 20, tNode.y, ybottom, false);
            } else {
                nodeLeft = this.processBackendJsonNode(backnode.left, xleft, tNode.x, tNode.y, ybottom, false);
            }
            this.links.push(new Link(tNode, nodeLeft, this.draw_params, true));
            tNode.left = nodeLeft;
        } else if (canaddnodes) {
            var tBut = new SquareButton(x=tNode.x - circlediff - this.buttonSideLength,
                y=tNode.y + circlediff,
                id=backnode.id,
                type="add",
                isLeft=true,
                params=this.draw_params,
                altx=tNode.x - altcirclediff - this.buttonSideLength,
                alty=tNode.y + altcirclediff)
            this.squareButtons.push(tBut);
        }
        if (backnode.right != null) {
            nodeRight = this.processBackendJsonNode(backnode.right, tNode.x, xright, tNode.y, ybottom, false);
            this.links.push(new Link(tNode, nodeRight, this.draw_params, false));
            tNode.right = nodeRight;
        } else if (canaddnodes) {
            var tBut = new SquareButton(x=tNode.x + circlediff,
                y=tNode.y + circlediff, id=backnode.id, type="add", isLeft=false, params=this.draw_params,
                altx=tNode.x + altcirclediff, alty= tNode.y + altcirclediff)
            this.squareButtons.push(tBut);
        }
        if (candeletenodes) {
            var tBut = new SquareButton(x=tNode.x + circlediff, y=tNode.y - circlediff - this.buttonSideLength,
                id=backnode.id, type="del", isLeft=false, params=this.draw_params, altx=tNode.x + altcirclediff, alty=tNode.y - altcirclediff - this.buttonSideLength)
            this.squareButtons.push(tBut);
        }

        if (this.isPointerMode()) {
            if (isRoot) {
                // One button in the center
                // No alt coords given so it doesn't move on toggle
                var tBut = new SquareButton(x=tNode.x - (this.buttonSideLength / 2), y=tNode.y + circlediff,
                                            id=backnode.id, type="ptr", isLeft=true, params=this.draw_params)
                this.squareButtons.push(tBut);
            } else {
                // Left pointer button
                var tBut = new SquareButton(x = tNode.x - circlediff - this.buttonSideLength,
                    y=tNode.y + circlediff, id=backnode.id, type="ptr", isLeft=true, params=this.draw_params,
                    altx = tNode.x - altcirclediff - this.buttonSideLength, alty=tNode.y + altcirclediff)
                this.squareButtons.push(tBut);

                // Right pointer button
                var tBut = new SquareButton(x=tNode.x + circlediff, y=tNode.y + circlediff, id=backnode.id, type="ptr", id=false, params=this.draw_params,
                    altx=tNode.x + altcirclediff, y=tNode.y + altcirclediff)
                this.squareButtons.push(tBut);
            }
        }
    }

    if (this.editmode == "side-label") {
        tNode.frontText = backnode.frontLabel
    }

    return tNode;

}

// safe
function escapeHtml(unsafe)
{
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

// safe
function unescapeHtml(safe)
{
    return safe.toString()
         .replace(/&amp;/g, "&")
         .replace(/&lt;/g, "<")
         .replace(/&gt;/g, ">")
         .replace(/&quot;/g, '"')
         .replace(/&#039;/g, "'");
 }

 function escapeNode(node) {
    if (!node) {
        return
    }
    node.value = escapeHtml(node.value)
    if ("children" in node) {
        node.children.forEach(escapeNode)
    } else{
        escapeNode(node.left)
        escapeNode(node.right)
    }
 }

// OO read
 function unescapeNode(node) {
    if (!node) {
        return
    }
    node.value = unescapeHtml(node.value)
    if ("children" in node) {
        node.children.forEach(unescapeHtml)
    } else {
        unescapeNode(node.left)
        unescapeNode(node.right)
    }
 }
