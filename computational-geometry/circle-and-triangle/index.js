paper.setup(document.getElementById('my_canvas'));

class Circle {
    constructor(center, radius) {
        this.center = center;
        this.radius = radius;
    }
}

class Line {
    // ax + by = c
    constructor(A, B) {
        this.A = A;
        this.B = B;
        this.a = B.y - A.y;
        this.b = A.x - B.x;
        this.c = this.a * A.x + this.b * B.y;
    }

    makePerpendicular() {
        let M = {
            x: (this.A.x + this.B.x) / 2,
            y: (this.A.y + this.B.y) / 2
        };
        this.c = -this.b * M.x + this.a * M.y;
        const temp = this.a;
        this.a = -this.b;
        this.b = temp;
    }

    intersectionTo(other) {
        const det = this.a * other.b - other.a * this.b;
        const x = (other.b * this.c - this.b * other.c) / det;
        const y = (this.a * other.c - other.a * this.c) / det;
        return new paper.Point(x, y);
    }
}

class Triangle {
    constructor(a, b, c) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.path = new paper.Path();
        this.path.strokeColor = 'black';
        this.path.add(a);
        this.path.add(b);
        this.path.add(c);
        this.path.closed = true;
        this.path.selected = true;
    }

    ab() {
        return this.a.getDistance(this.b);
    }

    bc() {
        return this.b.getDistance(this.c);
    }

    ac() {
        return this.a.getDistance(this.c);
    }

    moveC(x, y) {
        this.c = new paper.Point(x, y);
        this.path.removeSegment(2);
        this.path.insert(2, this.c);
    }

    incC(incX, incY) {
        this.c = new paper.Point(this.c.x + incX, this.c.y + incY);
        this.path.removeSegment(2);
        this.path.insert(2, this.c);
    }

    inscribeCircle() {
        const ab = this.ab();
        const bc = this.bc();
        const ac = this.ac();
        const perimeter = ab + bc + ac;
        const center = new paper.Point(0, 0)
            .add(this.a.multiply(bc))
            .add(this.b.multiply(ac))
            .add(this.c.multiply(ab))
            .divide(perimeter);
        const radius = Math.sqrt(((-ab + bc + ac) * (ab - bc + ac) * (ab + bc - ac)) / (ab + bc + ac)) / 2;
        return new Circle(center, radius);
    }

    circumscribeCircle() {
        const ab = this.ab();
        const bc = this.bc();
        const ac = this.ac();
        const radius = (ab * bc * ac) / Math.sqrt((ab + bc + ac) * (-ab + bc + ac) * (ab - bc + ac) * (ab + bc - ac));
        const line1 = new Line(this.a, this.b);
        const line2 = new Line(this.b, this.c);
        line1.makePerpendicular();
        line2.makePerpendicular();
        const center = line1.intersectionTo(line2);
        return new Circle(center, radius)
    }
}

function main() {
    let triangle = new Triangle(
        new paper.Point(550, 50),
        new paper.Point(750, 300),
        new paper.Point(300, 250)
    );

    let path = new paper.Path();
    path.add(new paper.Point(300, 250));
    path.add(new paper.Point(250, 300));
    path.add(new paper.Point(200, 400));
    path.add(new paper.Point(500, 600));
    path.strokeColor = 'red';
    path.strokeWidth = 2;
    path.selected = true;

    let _circle = triangle.circumscribeCircle();
    let circle = new paper.Path.Circle(_circle.center, _circle.radius);
    circle.strokeColor = 'black';

    let segments = path.getSegments();
    let segmentIndex = 0;
    let nextSegmentIndex = 1;
    let point = segments[segmentIndex].point;
    let nextPoint = segments[nextSegmentIndex].point;
    let incX = (nextPoint.x - point.x) / 100;
    let incY = (nextPoint.y - point.y) / 100;
    let stop = false;

    paper.view.draw();
    paper.view.onFrame = function () {
        if (stop) {
            return;
        }

        triangle.incC(incX, incY);

        let newCircle = triangle.circumscribeCircle();
        circle.scale(newCircle.radius / _circle.radius);
        _circle.radius = newCircle.radius;
        circle.position = newCircle.center;

        if (!betweenPoints(triangle.path.getLastSegment().point, point, nextPoint)) {
            segmentIndex++;
            nextSegmentIndex++;
            if (nextSegmentIndex === segments.length) {
                stop = true;
                return;
            }
            point = segments[segmentIndex].point;
            nextPoint = segments[nextSegmentIndex].point;
            incX = (nextPoint.x - point.x) / 100;
            incY = (nextPoint.y - point.y) / 100;
        }
    };
}

function betweenPoints(target, a, b) {
    let x = target.x;
    let y = target.y;
    let x1 = a.x;
    let y1 = a.y;
    let x2 = b.x;
    let y2 = b.y;

    if (x1 > x2) {
        let temp = x1;
        x1 = x2;
        x2 = temp;
    }
    if (y1 > y2) {
        let temp = y1;
        y1 = y2;
        y2 = temp;
    }

    if (x < x1 || x > x2) {
        return false;
    }
    return !(y < y1 || y > y2);
}


main();
