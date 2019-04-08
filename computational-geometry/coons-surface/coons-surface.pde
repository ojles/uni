float[] x = {0, 300, 0, 0};
float[] y = {0, 0, 0, 300};
float[] z = {400, 0, 300, 0};
int choise = 0;

void setup() 
{ 
  size(1200, 600, P2D);
}

void draw() 
{ 
  background(255);
  pushMatrix();
  textSize(32);
  fill(255, 0 ,0);
  stroke(0);
  strokeWeight(2);
  scale(1.2);
  fill(120, 120, 120);
  translate(width/4, height/4);
  
  float step = 0.02;
  String axis = "";
  if (choise == 0)
  {
    axis = "x";
    for(float u = 0; u < 1; u += step)
       for(float w = 0; w < 1; w += step)
       {
          float[] quw = Q(u,w);
          point(quw[1], quw[2]);
       }
  }
  else if (choise == 1) 
  {
    axis = "y";
    for(float u = 0; u < 1; u += step)
      for(float w = 0; w < 1; w += step) 
      { 
          float[] quw = Q(u,w); 
          point(quw[0], quw[2]);
      }
  }
  else if (choise == 2)
  {
    axis = "z";
    for(float u = 0; u < 1; u += step)
       for(float w = 0; w < 1; w += step) 
       { 
          float[] quw = Q(u,w); 
          point(quw[0], quw[1]);
       }
  }
  translate(-200, -200);
  text(axis + "=0", 100, 100);
  popMatrix();
}
  
void mousePressed()
{
  choise = (choise + 1) % 3;
}

float[] Q(float u, float w) 
{
   float[] _P0w = P0w(w); 
   float[] _P1w = P1w(w);
   float[] _P0u = Pu0(u); 
   float[] _P1u = Pu1(u);
   return new float[] {
       _P0u[0] * (1-w) + _P1u[0] * w + _P0w[0] * (1-u) + _P1w[0] * u - x[0] * (1-u) * (1-w) - x[1] * (1-u) * w - x[2] * u * (1-w) - x[3] * u * w,
       _P0u[1] * (1-w) + _P1u[1] * w + _P0w[1] * (1-u) + _P1w[1] * u - y[0] * (1-u) * (1-w) - y[1] * (1-u) * w - y[2] * u * (1-w) - y[3] * u * w,
       _P0u[2] * (1-w) + _P1u[2] * w + _P0w[2] * (1-u) + _P1w[2] * u - z[0] * (1-u) * (1-w) - z[1] * (1-u) * w - z[2] * u * (1-w) - z[3] * u * w
   };
}

float[] P0w(float t) 
{ 
  return new float[] {
    x[0] + t * (x[1] - x[0]), y[0] + t * (y[1] - y[0]), z[0] + t * (z[1] - z[0])
  };
} 

float[] P1w(float t) 
{ 
  return new float[] {
    x[2] + t * (x[3] - x[2]), y[2] + t * (y[3] - y[2]), z[2] + t * (z[3] - z[2])
  };
} 

float[] Pu0(float t) 
{ 
  return new float[] {
    x[0] + t * (x[1] - x[0]), y[0] + t * (y[1] - y[0]), z[0] + t * (z[1] - z[0])
  };
} 

float[] Pu1(float t) 
{ 
  return new float[] {
    x[2] + t * (x[3] - x[2]), y[2] + t * (y[3] - y[2]), z[2] + t * (z[3] - z[2])
  };
}
