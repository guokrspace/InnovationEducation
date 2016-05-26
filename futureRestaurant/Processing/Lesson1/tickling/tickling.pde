int inflation = 10;
String button = "Button";
int x=width/2;
int y=height/2;

void setup()
{
   x=width/2;  
   y=height/2;

   size(640,480);
}

void draw()
{
    background(0);
    
    stroke(0);
    fill(100,0,0);

    ellipse(x, y, inflation, inflation);
    
    inflation += 10;
    
    if(inflation > 500)
    {
       inflation = 20; 
    }
    
    fill(#cccccc);
    rect(width/2-100, height/2-50, 200, 100);
    
    fill(0);
    textSize(50);
    textAlign(CENTER);
    text("Button", width/2, height/2+20);
    
    if(mouseX > width/2-100 && mouseX < width/2 +100)
    {
      if(mouseY > height/2-50 && mouseY <   height/2 + 50)
      {
        x += random(-10, 10);
        y += random(-10, 10);
      }
    }
}