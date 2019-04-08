final int HEIGHT = 600;
final int WIDTH = 600;

final int LEFT = 1;
final int RIGHT = 2;
final int BOTTOM = 4;
final int TOP = 8;

int vcode(Rectangle r, Point point) {
  int code = 0;
  if (point.x < r.minX) {
    code |= LEFT;
  } else if (point.x > r.maxX) {
    code |= RIGHT;
  } else if (point.y < r.minY) {
    code |= BOTTOM;
  } else if (point.y > r.maxY) {
    code |= TOP;
  }
  return code;
}

List<Line> cohenSutherland(Rectangle r, Line originalLine) {
  Line line = originalLine.clone();
  Point a = line.a;
  Point b = line.b;
  
  int acode = vcode(r, a);
  int bcode = vcode(r, b);
  
  Point c;
  int ccode;
  
  List<Line> cutLines = new ArrayList<Line>();
  
  while ((acode | bcode) != 0) {
    if ((acode & bcode) != 0) {
      return Arrays.asList(originalLine);
    }
    
    if (acode != 0) {
      ccode = acode;
      c = a.clone();
    } else {
      ccode = bcode;
      c = b.clone();
    }
    
    if ((ccode & LEFT) != 0) {
      c.y += (a.y - b.y) * (r.minX - c.x) / (a.x - b.x);
      c.x = r.minX;
    } else if ((ccode & RIGHT) != 0) {
      c.y += (a.y - b.y) * (r.maxX - c.x) / (a.x - b.x);
      c.x = r.maxX;
    } else if ((ccode & TOP) != 0) {
      c.x += (a.x - b.x) * (r.maxY - c.y) / (a.y - b.y);
      c.y = r.maxY;
    } else if ((ccode & BOTTOM) != 0) {
      c.x += (a.x - b.x) * (r.minY - c.y) / (a.y - b.y);
      c.y = r.minY;
    }
    
    if (ccode == acode) {
      cutLines.add(new Line(a.x, a.y, c.x, c.y));
      a.changeTo(c);
      acode = vcode(r, a);
    } else {
      cutLines.add(new Line(b.x, b.y, c.x, c.y));
      b.changeTo(c);
      bcode = vcode(r, b);
    }
  }

  line.draw();
  return cutLines;
}
