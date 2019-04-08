class Point {
  public float x;
  public float y;
  
  public Point(float x, float y) {
    this.x = x;
    this.y = y;
  }
  
  public Point plusX(float amount) {
    x += amount;
    return this;
  }
  
  public Point plusY(float amount) {
    y += amount;
    return this;
  }
  
  public void changeTo(Point other) {
    x = other.x;
    y = other.y;
  }
  
  public void draw(int size) {
    ellipse(x, y, size, size);
  }
  
  public Point clone() {
    return new Point(x, y);
  }
}

class Line {
  public Point a;
  public Point b;
  
  public Line(float ax, float ay, float bx, float by) {
    this(new Point(ax, ay), new Point(bx, by));
  }
  
  public Line(Point a, Point b) {
    this.a = a;
    this.b = b;
  }
  
  public void draw() {
    a.draw(4);
    b.draw(4);
    line(a.x, a.y, b.x, b.y);
  }
  
  public Line clone() {
    return new Line(a.x, a.y, b.x, b.y);
  }
}

class Rectangle {
  public float minX;
  public float minY;
  public float maxX;
  public float maxY;
  
  public float width;
  public float height;
  
  public Rectangle(Point corner, float width, float height) {
    this.width = width;
    this.height = height;
    this.minX = corner.x;
    this.minY = corner.y;
    this.maxX = minX + width;
    this.maxY = minY + height;
  }
  
  public void draw() {
    rect(minX, minY, width, height);
  }
}

class Color {
  public int r;
  public int g;
  public int b;
  
  public Color(int r, int g, int b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }
}
