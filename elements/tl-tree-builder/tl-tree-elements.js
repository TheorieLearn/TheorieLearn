// Helper Math Functions
function det(a, b, c, d, e, f, g, h, i) {
	return a * e * i + b * f * g + c * d * h - a * f * h - b * d * i - c * e * g;
}

function circleFromThreePoints(x1, y1, x2, y2, x3, y3) {
	var a = det(x1, y1, 1, x2, y2, 1, x3, y3, 1);
	var bx = -det(x1 * x1 + y1 * y1, y1, 1, x2 * x2 + y2 * y2, y2, 1, x3 * x3 + y3 * y3, y3, 1);
	var by = det(x1 * x1 + y1 * y1, x1, 1, x2 * x2 + y2 * y2, x2, 1, x3 * x3 + y3 * y3, x3, 1);
	var c = -det(x1 * x1 + y1 * y1, x1, y1, x2 * x2 + y2 * y2, x2, y2, x3 * x3 + y3 * y3, x3, y3);
	return {
		'x': -bx / (2 * a),
		'y': -by / (2 * a),
		'radius': Math.sqrt(bx * bx + by * by - 4 * a * c) / (2 * Math.abs(a))
	};
}

function Node(x, y, params) {
    this.x = x;
    this.y = y;
	this.point = false; // reduces the radius to a dot
	this.visible = true; // draws the node
	this.decoration = false; // Makes the node unselectable
	this.square = false; // draws it as a square in every editmode
    this.mouseOffsetX = 0;
    this.mouseOffsetY = 0;
    this.text = '';
	this.id = Infinity; //Anything that doesn't explicitly set an id doesn't need to be found
	this.isAcceptState = false; // Gives the accept state visual from the FSM builder, otherwise called "highlight" here
	this.isSubTree = false;
	this.isSubSubTree = false;
	this.p = params;
	this.isSelected = false;
	this.frontText = "";
}

function PointNode(x, y, params, visible=false) {
	let node = new Node(x, y, params);
	node.point = true;
	node.visible = visible;
	node.decoration = true;
	return node;
}

Node.prototype.setMouseStart = function (x, y) {
    this.mouseOffsetX = this.x - x;
    this.mouseOffsetY = this.y - y;
};

Node.prototype.setAnchorPoint = function (x, y) {
    this.x = x + this.mouseOffsetX;
    this.y = y + this.mouseOffsetY;
};

// TODO nodeRadius, selectedObject, node_mode, editmode, rootptr
Node.prototype.draw = function (c) {
	let nodeRadius = this.p.nodeRadius
	let node_mode = this.p.node_mode
	let editmode = this.p.editmode
	let rootptr = this.p.rootptr
	let draw_caret = this.p.draw_caret
	let selected = this.isSelected
	let text = this.text

	if (!this.visible) {
		return;
	}

	if (!(editmode == "pointer" && this.text == rootptr)) {
		if (this.isSubTree && node_mode == "circle" || !this.isSubTree && node_mode=="triangle") {
			c.beginPath()
			c.moveTo(this.x, this.y - (nodeRadius * Math.sqrt(3)))
			c.lineTo(this.x - (Math.sqrt(2) * nodeRadius), this.y + (Math.sqrt(2) * nodeRadius / 2))
			c.lineTo(this.x + (Math.sqrt(2) * nodeRadius), this.y + (Math.sqrt(2) * nodeRadius / 2))
			c.closePath();
			c.stroke()
		} else if (this.square || (!this.isSubTree && node_mode == "square")) {
			c.beginPath()
			c.rect(this.x - nodeRadius, this.y- nodeRadius, nodeRadius*2, nodeRadius*2)
			c.stroke()
		} else if ((this.isSubTree && (node_mode == "square" || node_mode == "triangle")) || this.isSubSubTree) {
			c.beginPath()
			c.rect(this.x - (2*nodeRadius), this.y- nodeRadius, nodeRadius*4, nodeRadius*2)
			c.stroke()
		} else if (this.point) {
			c.beginPath()
			c.arc(this.x, this.y, 2, 0, 2*Math.PI, false)
			c.fill()
			c.stroke()
		} else {
			// draw the circle
			c.beginPath();
			c.arc(this.x, this.y, nodeRadius, 0, 2 * Math.PI, false);
			c.stroke();
			// draw a double circle for an accept state
			if (this.isAcceptState) {
				c.beginPath();
				c.arc(this.x, this.y, nodeRadius - 6, 0, 2 * Math.PI, false);
				c.stroke();
			}
		}
	}

	if (editmode == "side-label") {
		c.beginPath()
		c.rect(this.x + (nodeRadius * Math.sqrt(2) / 2), this.y- (nodeRadius * Math.sqrt(2) / 2) - nodeRadius, nodeRadius, nodeRadius)
		c.stroke()
		drawText(c, text, this.x + (nodeRadius * (1 + Math.sqrt(2)) / 2), this.y- (nodeRadius * (1 + Math.sqrt(2)) / 2), null, selected, nodeRadius / 2, draw_caret);
		selected = false
		draw_caret = false
		text = this.frontText
	}

    // draw the text
    drawText(c, text, this.x, this.y, null, selected, nodeRadius, draw_caret);
	if (this.isSubSubTree) {
		c.strokeText("Repeat", this.x - (nodeRadius), this.y - nodeRadius / 2, nodeRadius * 2)
		c.strokeText("Times", this.x - (nodeRadius), this.y + 0.7*nodeRadius, nodeRadius * 2)
	}
};

// TODO nodeRadius
Node.prototype.closestPointOnCircle = function (x, y) {
	let nodeRadius = this.p.nodeRadius;
    var dx = x - this.x;
    var dy = y - this.y;
    var scale = Math.sqrt(dx * dx + dy * dy);
    return {
        'x': this.x + dx * nodeRadius / scale,
        'y': this.y + dy * nodeRadius / scale,
    };
};

Node.prototype.containsPoint = function (x, y) {
	let nodeRadius = this.p.nodeRadius
	let inNode = (x - this.x) * (x - this.x) + (y - this.y) * (y - this.y) < nodeRadius * nodeRadius
	let squarex = this.x + (nodeRadius * Math.sqrt(2) / 2)
	let squarey = this.y- (nodeRadius * Math.sqrt(2) / 2) - nodeRadius
	let inSideLabel = squarex <= x && x <= squarex + nodeRadius && squarey <= y && y <= squarey + nodeRadius;
    return inNode || (this.p.editmode == "side-label" && inSideLabel);
};

function SquareButton(x, y, id, type, isLeft, params, altX=-1, altY=-1) {
	//Coordinates of topleft corner
	this.x = x;
	this.y = y;
	this.id = id;
	this.type = type; // can be "add" "del" "ptr" "exp" "con"
	this.isLeft = isLeft;
	// Coordinates to shift to on "Toggle Node Size"
	this.altx = altX == -1 ? x : altX;
	this.alty = altY == -1 ? y : altY;
	this.p = params;
}

// Basically the whole reason why we're having the square button keep track of two locations is for
// When we do toggle node size. In builder mode, you can safely just call processBackendJson() again
// And then redraw so all the squarebuttons will be updated according to the correct node size.
// However, with pointer mode, we can't call processBackendJson except at the beginning because it will
// Wipe the front end which causes problems if the student is in the middle of manipulating pointers
// Without updating. So this just has the squareButtons keep track of two locations from creation so then
// ProcessBackendJson never needs to get called in toggle node size.s
SquareButton.prototype.toggleloc = function () {
	let oldx = this.x;
	let oldy = this.y;
	this.x = this.altx;
	this.y = this.alty;
	this.altx = oldx;
	this.alty = oldy;
	this.isSelected = false;
}

// TODO buttonSideLength
SquareButton.prototype.containsPoint = function (x, y) {
	let buttonSideLength = this.p.buttonSideLength
	return this.x <= x && x <= this.x + buttonSideLength && this.y <= y && y <= this.y + buttonSideLength;
}

// TODO uses buttonSideLength
SquareButton.prototype.draw = function (c) {
	let buttonSideLength = this.p.buttonSideLength;
	if (this.type == "add") {
		c.fillStyle = c.strokeStyle = 'rgb(0, 155, 0)'; // should be dark green
		drawText(c, "+", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false, this.p.nodeRadius, this.p.draw_caret);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	} else if (this.type == "del") {
		c.fillStyle = c.strokeStyle = 'rgb(155, 0, 0)'; // dark red
		drawText(c, "X", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false, this.p.nodeRadius, this.p.draw_caret);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	} else if (this.type == "ptr") {
		c.fillStyle = c.strokeStyle = 'rgb(103, 52, 235)'; // Light Purple
		if (this.isSelected) {
			c.fillRect(this.x, this.y, buttonSideLength, buttonSideLength)
		} else {
			c.beginPath();
			c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
			c.stroke()
		}
	} else if (this.type == "exp") {
		c.fillStyle = c.strokeStyle = 'rgb(255, 120, 3)'; // Orange
		drawText(c, "↔", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false, this.p.nodeRadius, this.p.draw_caret);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	}
	else if (this.type == "con") {
		c.fillStyle = c.strokeStyle = 'rgb(3, 125, 255)'; // blue
		drawText(c, ">-<", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false, this.p.nodeRadius, this.p.draw_caret);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	}
}

function Link(a, b, params, leftlink) {
	this.nodeA = a;
	this.nodeB = b;

	this.isLeftLink = leftlink;

	this.editable = false;
	this.text = "";
	this.isHeightLink = false;
	this.lineAngleAdjust = 0; // value to add to textAngle when link is straight line

	// make anchor point relative to the locations of nodeA and nodeB
	this.parallelPart = 0.5; // percentage from nodeA to nodeB
	this.perpendicularPart = 0; // pixels from line between nodeA and nodeB

	this.p = params
}

// TODO accesses editmode, node_mode, nodeRadius
Link.prototype.getEndPointsAndCircle = function () {
	let nodeRadius = this.p.nodeRadius;
	let node_mode = this.p.node_mode;
	let editmode = this.p.editmode;
	if (this.perpendicularPart == 0) {
		var midX = (this.nodeA.x + this.nodeB.x) / 2;
		var midY = (this.nodeA.y + this.nodeB.y) / 2;
		if (node_mode == "square") {
			var start = {'x': this.nodeA.x, 'y': this.nodeA.y + nodeRadius}
		} else if (node_mode == "triangle") {
			var start = {'x': this.nodeA.x, 'y': this.nodeA.y + (nodeRadius * Math.sqrt(2) / 2)}
		} else {
			var start = this.nodeA.closestPointOnCircle(midX, midY);
		}
		if (node_mode == "square" || (node_mode == "triangle" && this.nodeB.isSubTree)) {
			var end = {'x': this.nodeB.x, 'y': this.nodeB.y - nodeRadius}
		} else if ((node_mode == "triangle" && !this.nodeB.isSubTree) || (node_mode == "circle" && this.nodeB.isSubTree)) {
			var end = {'x': this.nodeB.x, 'y': this.nodeB.y - (nodeRadius * Math.sqrt(3))};
		} else {
			var end = this.nodeB.closestPointOnCircle(midX, midY);
		}

		if (editmode == "pointer") {
			let circlediff = 2 ** (-0.5) * nodeRadius
			// In the bottom left if edge from left side, bottom right if edge from right side, In the middle if this is Rootptr
			let factor = this.nodeA.text == this.p.rootptr ? 0 : (this.isLeftLink ? -1 : 1)
			start = {
				'x': this.nodeA.x + (factor * circlediff),
				'y': this.nodeA.y + circlediff
			}
		}

		if (this.nodeA.point) {
			start = {'x': this.nodeA.x, 'y': this.nodeA.y};
		}
		if (this.nodeB.point) {
			end = {'x': this.nodeB.x, 'y': this.nodeB.y};
		}

		return {
			'hasCircle': false,
			'startX': start.x,
			'startY': start.y,
			'endX': end.x,
			'endY': end.y,
		};
	}
	var anchor = this.getAnchorPoint();
	var circle = circleFromThreePoints(this.nodeA.x, this.nodeA.y, this.nodeB.x, this.nodeB.y, anchor.x, anchor.y);
	var isReversed = (this.perpendicularPart > 0);
	var reverseScale = isReversed ? 1 : -1;
	var startAngle = Math.atan2(this.nodeA.y - circle.y, this.nodeA.x - circle.x) - reverseScale * nodeRadius / circle.radius;
	var endAngle = Math.atan2(this.nodeB.y - circle.y, this.nodeB.x - circle.x) + reverseScale * nodeRadius / circle.radius;
	var startX = circle.x + circle.radius * Math.cos(startAngle);
	var startY = circle.y + circle.radius * Math.sin(startAngle);
	var endX = circle.x + circle.radius * Math.cos(endAngle);
	var endY = circle.y + circle.radius * Math.sin(endAngle);
	return {
		'hasCircle': true,
		'startX': startX,
		'startY': startY,
		'endX': endX,
		'endY': endY,
		'startAngle': startAngle,
		'endAngle': endAngle,
		'circleX': circle.x,
		'circleY': circle.y,
		'circleRadius': circle.radius,
		'reverseScale': reverseScale,
		'isReversed': isReversed,
	};
};

// TODO compares to selectedobject
Link.prototype.draw = function (c) {
	var stuff = this.getEndPointsAndCircle();
    // TODO: Simplify this. we don't need to handle arcs.
	// draw arc
	c.beginPath();
	if (stuff.hasCircle) {
		c.arc(stuff.circleX, stuff.circleY, stuff.circleRadius, stuff.startAngle, stuff.endAngle, stuff.isReversed);
	} else {
		c.moveTo(stuff.startX, stuff.startY);
		c.lineTo(stuff.endX, stuff.endY);
	}
	c.stroke();
	// draw the head of the arrow
	if (stuff.hasCircle) {
		drawArrow(c, stuff.endX, stuff.endY, stuff.endAngle - stuff.reverseScale * (Math.PI / 2));
	} else {
		drawArrow(c, stuff.endX, stuff.endY, Math.atan2(stuff.endY - stuff.startY, stuff.endX - stuff.startX));
	}

	// draw the text
	if (stuff.hasCircle) {
		var startAngle = stuff.startAngle;
		var endAngle = stuff.endAngle;
		if (endAngle < startAngle) {
			endAngle += Math.PI * 2;
		}
		var textAngle = (startAngle + endAngle) / 2 + stuff.isReversed * Math.PI;
		var textX = stuff.circleX + stuff.circleRadius * Math.cos(textAngle);
		var textY = stuff.circleY + stuff.circleRadius * Math.sin(textAngle);
		// Assume links can't be selected (they can't currently)
		drawText(c, this.text, textX, textY, textAngle, false, this.p.nodeRadius, this.p.draw_caret);
	} else {
		var textX = (stuff.startX + stuff.endX) / 2;
		var textY = (stuff.startY + stuff.endY) / 2;
		var textAngle = Math.atan2(stuff.endX - stuff.startX, stuff.startY - stuff.endY);
		// Assume links can't be selected (they can't currently)
		drawText(c, this.text, textX, textY, textAngle + this.lineAngleAdjust, false, this.p.nodeRadius, this.p.draw_caret);
	}
};

Link.prototype.containsPoint = function (x, y) {
	var stuff = this.getEndPointsAndCircle();
	if (stuff.hasCircle) {
		var dx = x - stuff.circleX;
		var dy = y - stuff.circleY;
		var distance = Math.sqrt(dx * dx + dy * dy) - stuff.circleRadius;
		if (Math.abs(distance) < hitTargetPadding) {
			var angle = Math.atan2(dy, dx);
			var startAngle = stuff.startAngle;
			var endAngle = stuff.endAngle;
			if (stuff.isReversed) {
				var temp = startAngle;
				startAngle = endAngle;
				endAngle = temp;
			}
			if (endAngle < startAngle) {
				endAngle += Math.PI * 2;
			}
			if (angle < startAngle) {
				angle += Math.PI * 2;
			} else if (angle > endAngle) {
				angle -= Math.PI * 2;
			}
			return (angle > startAngle && angle < endAngle);
		}
	} else {
		var dx = stuff.endX - stuff.startX;
		var dy = stuff.endY - stuff.startY;
		var length = Math.sqrt(dx * dx + dy * dy);
		var percent = (dx * (x - stuff.startX) + dy * (y - stuff.startY)) / (length * length);
		var distance = (dx * (y - stuff.startY) - dy * (x - stuff.startX)) / length;
		return (percent > 0 && percent < 1 && Math.abs(distance) < hitTargetPadding);
	}
	return false;
};

window.TreeBuilderElement.prototype.genEllipsis = function(startx, starty, endx, endy, parent=null, minDots=0) {
	let dist = Math.sqrt((endy - starty) **2 + (endx -startx)**2)
	if (dist < 2*this.largeNodeSize && minDots == 0) {return;}
	let dots = Math.max(dist / (1.7*this.largeNodeSize), minDots);
	for (let i = 0; i < dots; i++) {
		let x = startx + i * (endx - startx) / dots;
		let y = starty + i * (endy - starty) / dots;
		point = PointNode(x, y, this.draw_params, true)
		this.nodes.push(point)
		if (parent != null) {
			this.links.push(new Link(parent, point, this.draw_params, true))
		}
	}
}

function drawText(c, originalText, x, y, angleOrNull, isSelected, nodeRadius, drawCaret) {
    text = originalText
    //text = convertLatexShortcuts(originalText);
    c.font = '20px "Times New Roman", serif';
    var width = c.measureText(text).width;

    // Attempt to keep text within the bounds of the node
    if (width > nodeRadius + 16) {
        var newpx = 20 - parseInt((width - nodeRadius) / 8);
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

        if (drawCaret && isSelected && caretVisible && canvasHasFocus() && document.hasFocus()) {
            x += width;
            c.beginPath();
            c.moveTo(x, y - 10);
            c.lineTo(x, y + 10);
            c.stroke();
        }
    }
}
