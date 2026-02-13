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

function Node(x, y) {
    this.x = x;
    this.y = y;
    this.mouseOffsetX = 0;
    this.mouseOffsetY = 0;
    this.text = [''];
	this.id = 0;
	this.isAcceptState = false; // Gives the accept state visual from the FSM builder, otherwise called "highlight" here
	this.isSubTree = false;
	this.index = 0;
	this.canAddNodes = false;
	this.canDeleteNodes = false;
	this.canPromoteNodes = false;
	this.canDemoteNodes = false;
	this.wouldDemoteNodes = false;
	this.drawChildSelected = false;
	this.drawParentSelected = false;
}

Node.prototype.setMouseStart = function (x, y) {
    this.mouseOffsetX = this.x - x;
    this.mouseOffsetY = this.y - y;
};

Node.prototype.setAnchorPoint = function (x, y) {
    this.x = x + this.mouseOffsetX;
    this.y = y + this.mouseOffsetY;
};

Node.prototype.draw = function (c) {
	if (this.drawChildSelected) {
		var color = 'rgb(103, 52, 235)' //Light purple
		c.lineWidth = 3
		c.fillStyle = c.strokeStyle = color
	} else if (this.drawParentSelected) {
		var color = 'rgb(252, 165, 3)'; // orange
		c.lineWidth = 3
		c.fillStyle = c.strokeStyle = color
	} else {
		var color = 'black'
		c.lineWidth = 1
		c.fillStyle = c.strokeStyle = color
	}
	for (var i = 0; i < this.text.length; i++) {

		var x = this.x + (i * nodeXSidelength);
		// draw the rect
		c.beginPath();
		c.rect(x, this.y, nodeXSidelength, nodeYSidelength);
		c.stroke();
		// draw a double rect for an accept state
		if (this.isAcceptState) {
			c.beginPath();
			c.rect(x + nodeXSidelength * .2, this.y + nodeYSidelength * .2, nodeXSidelength * .6, nodeYSidelength * .6);
			c.stroke()
		}

		// draw the text
		drawText(c, this.text[i], x + nodeXSidelength / 2, this.y + nodeYSidelength / 2, null, (selectedObject == this) && (selectedIndex == i));
		this.drawChildSelected  = false
		this.drawParentSelected = false
	}
	if (this == selectedObject) {
		color = 'rgb(51, 180, 255)' //Light blue
		c.lineWidth = 3
		c.fillStyle = c.strokeStyle = color
		var x = this.x + (selectedIndex * nodeXSidelength);
		c.beginPath();
		c.rect(x, this.y, nodeXSidelength, nodeYSidelength);
		c.stroke();
		// draw a double circle for an accept state
		if (this.isAcceptState) {
			c.beginPath();
			c.rect(x + nodeXSidelength * .2, this.y + nodeYSidelength * .2, nodeXSidelength * .6, nodeYSidelength * .6);
			c.stroke()
		}
	}

};

Node.prototype.closestPointOnCircle = function (x, y) {
    var dx = x - this.x;
    var dy = y - this.y;
    var scale = Math.sqrt(dx * dx + dy * dy);
    return {
        'x': this.x + dx * nodeRadius / scale,
        'y': this.y + dy * nodeRadius / scale,
    };
};

Node.prototype.containsPoint = function (x, y) {
    return this.x <= x && x <= this.x + (nodeXSidelength * this.text.length) && this.y <= y && y <= this.y + nodeYSidelength;
};

// assumes containsPoint is true
Node.prototype.indexContainsPoint = function (x) {
	for (var i = 0; i < this.text.length; i++) {
		if (x < this.x  + ((i + 1) * nodeXSidelength)) {
			return i;
		}
	}
	return 0;
}

// Different from standard tree builder, x and y are the coordinates of the parent node, not the actual button
// solves for correct loc here which is saved as this.x, this.y
function SquareButton(x, y, id, type, isLeft, index=0) {
	//Coordinates of topleft corner
	this.x = x + (nodeXSidelength * (index + (isLeft ? 0 : 1) + ((type == "pro") || (type == "dem") ? (-1/2) : 0))) - (buttonSideLength / (type == 'del' ? 1 : 2));
	this.y = y + (type == "add" || type == "dem" ? nodeYSidelength : 0) + (type == "pro" ? -1 * buttonSideLength : 0);
	this.id = id;
	this.index = index;
	this.type = type // can be "add" "del" "ptr" "up" "pro" "dem"
	this.isLeft = isLeft;
}

SquareButton.prototype.containsPoint = function (x, y) {
	return this.x <= x && x <= this.x + buttonSideLength && this.y <= y && y <= this.y + buttonSideLength;
}

SquareButton.prototype.draw = function (c) {
	if (this.type == "add") {
		c.fillStyle = c.strokeStyle = 'rgb(0, 155, 0)'; // should be dark green
		drawText(c, "+", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	} else if (this.type == "del") {
		c.fillStyle = c.strokeStyle = 'rgb(155, 0, 0)'; // dark red
		drawText(c, "X", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	} else if (this.type == "ptr") {
		c.fillStyle = c.strokeStyle = 'rgb(103, 52, 235)'; // Light Purple
		if (this == selectedObject) {
			c.fillRect(this.x, this.y, buttonSideLength, buttonSideLength)
		} else {
			c.beginPath();
			c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
			c.stroke()
		}
	} else if (this.type == "pro") {
		c.fillStyle = c.strokeStyle = 'rgb(0, 0, 255)'; // dark blue
		drawText(c, "↑", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	} else if (this.type == "dem") {
		c.fillStyle = c.strokeStyle = 'rgb(252, 165, 3)'; // orange
		drawText(c, "↓", this.x + (buttonSideLength / 2), this.y + buttonSideLength / 2, null, false);

		c.beginPath();
		c.rect(this.x, this.y, buttonSideLength, buttonSideLength);
		c.stroke()
	}
}

function Link(a, b, leftlink) {
	this.nodeA = a;
	this.nodeB = b;

	this.isLeftLink = leftlink;

	// make anchor point relative to the locations of nodeA and nodeB
	this.parallelPart = 0.5; // percentage from nodeA to nodeB
	this.perpendicularPart = 0; // pixels from line between nodeA and nodeB
}

Link.prototype.getEndPointsAndCircle = function () {
	if (this.perpendicularPart == 0) {
		var midX = (this.nodeA.x + this.nodeB.x) / 2;
		var midY = (this.nodeA.y + this.nodeB.y) / 2;
		var start = {
			'x': this.nodeA.x + (nodeXSidelength * this.nodeB.index),
			'y': this.nodeA.y + nodeYSidelength,
		};
		var end = {
			'x': this.nodeB.x + (nodeXSidelength * this.nodeB.text.length / 2),
			'y': this.nodeB.y,
		};
		if (this.nodeB.isSubTree) {
			end = {
				'x': this.nodeB.x,
				'y': this.nodeB.y - (nodeRadius * Math.sqrt(3)),
			};
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

Link.prototype.draw = function (c) {
	if (this.nodeB == selectedObject) {
		c.lineWidth = 3;
		var color = 'rgb(103, 52, 235)' //Light purple
		c.fillStyle = c.strokeStyle = color
		this.nodeA.drawChildSelected = true
	} else if (this.nodeA == selectedObject && (this.nodeB.index == selectedIndex || this.nodeB.index == selectedIndex + 1)) {
		c.lineWidth = 3;
		var color = 'rgb(252, 165, 3)'; // orange
		c.fillStyle = c.strokeStyle = color
		this.nodeB.drawParentSelected = true
	} else {
		c.lineWidth = 1;
		var color = 'black'
		c.fillStyle = c.strokeStyle = color
	}


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
		drawText(c, this.text, textX, textY, textAngle, selectedObject == this);
	} else {
		var textX = (stuff.startX + stuff.endX) / 2;
		var textY = (stuff.startY + stuff.endY) / 2;
		var textAngle = Math.atan2(stuff.endX - stuff.startX, stuff.startY - stuff.endY);
		drawText(c, this.text, textX, textY, textAngle + this.lineAngleAdjust, selectedObject == this);
	}
};

function TemporaryLink(node, from, to){
    this.parent = node;
    this.from = from;
    this.to = to;
}
TemporaryLink.prototype.draw = function (c) {
	// draw the line
    var angle = Math.atan2(this.to.y - this.parent.y, this.to.x - this.parent.x);
	c.beginPath();
	c.moveTo(this.to.x - Math.cos(angle)*nodeRadius, this.to.y - Math.sin(angle)*nodeRadius);
	c.lineTo(this.parent.x + Math.cos(angle)*nodeRadius, this.parent.y + Math.sin(angle)*nodeRadius);
	c.moveTo(this.to.x+nodeRadius, this.to.y)
	c.arc(this.to.x, this.to.y, nodeRadius, 0, 2 * Math.PI, false);
    c.stroke();
	drawArrow(c, this.to.x - Math.cos(angle)*nodeRadius, this.to.y - Math.sin(angle)*nodeRadius, angle);
};
