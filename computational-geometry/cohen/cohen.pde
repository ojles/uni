import java.util.*; //<>//

void setup() {
  size(600, 600);
  background(255);
  drawOnce();
}

void drawOnce() {
  Rectangle rectangle1 = new Rectangle(new Point(WIDTH/4, HEIGHT/4), WIDTH/2, HEIGHT/2);
  Rectangle rectangle2 = new Rectangle(new Point(50, 10), WIDTH/3, HEIGHT - 100);
  
  Rectangle[] rectangles = new Rectangle[] {
    rectangle2,
    rectangle1
  };
  
  Color[] colors = new Color[] {
    new Color(255, 0, 0),
    new Color(0, 255, 0),
    new Color(0, 0, 255)
  };
  
  final Line[] lines = new Line[] {
    new Line(20, 200, 300, 60),
    new Line(500, 200, 550, 430),
    new Line(300, 400, 400, 230),
    new Line(340, 70, 230, 530),
    new Line(310, 510, 470, 360),
    new Line(10, 300, 300, 330)
  };

  for (int i = rectangles.length - 1; i >= 0; i--) {
    rectangles[i].draw();
  }
  for (Line line : lines) {
    line.draw();
  }
  
  List<Line> cutLines = Arrays.asList(lines);
  for (int i = 0; i < rectangles.length; i++) {
    Color c = colors[i];
    stroke(c.r, c.g, c.b);
    cutLines = cutLinesByRectangle(rectangles[i], cutLines);
  }
  drawLines(cutLines, colors[rectangles.length]);
}

List<Line> cutLinesByRectangle(Rectangle r, List<Line> lines) {
  List<Line> cutLines = new ArrayList<Line>();
  for (Line line : lines) {
    cutLines.addAll(cohenSutherland(r, line));
  }
  return cutLines;
}

void drawLines(List<Line> lines, Color c) {
  stroke(c.r, c.g, c.b);
  for (Line line : lines) {
    line.draw();
  }
}

void draw() {
  // ignore
}
