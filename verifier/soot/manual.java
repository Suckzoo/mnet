public class Manual {
  public void signature() {
    
  }
  public void testMe(int x, int y, int z) {
    if(x == 30) {
      if(y == 10) {
        if(z == 15) {
          System.out.print("X = 30 and Y = 10 and Z == 15");
        }
      }
    }
    if(x > 0){
      if(x < 35){
        x = x-1;
        if(y < 0){
          if(z > 30){
            System.out.print("1");;
          }
          else if(z < 30){
            System.out.print("2");;
          }
        }
        else if(y > 0){
          if(z > 30){
            System.out.print("3");;
            signature();
          }
          else if(z < 30){
            System.out.print("4");;
          }
        }
      }
      else if(x > 35){
        x = x-2;
        if(y < 0){
          if(z > 30){
            System.out.print("5");;
          }
          else if(z < 30){
            System.out.print("6");;
          }
        }
        else if(y > 0){
          if(z > 30){
            System.out.print("7");;
          }
          else if(z < 30){
            System.out.print("8");;
          }
        }
      }
      else{
        System.out.print("NA");
      }
    }
  }
}