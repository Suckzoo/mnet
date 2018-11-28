public class Manual2 {
  public void signature() {

  }
  public void testMe(int x, int y, int z) {
    y = y-1;
    x = y + z;
    z = z + 1;
    int d = x+y+z;
    
    if(d > 10){
      if( y > z){
        if(z == x){
          if(y > 10) {
            System.out.print("aa");
          }
        }
      } else {
        if ( x == 10){
          y = z;
          if(z > 20){
            System.out.print("aa");
            signature(); 
          }
        }
      }
    }

  }
}