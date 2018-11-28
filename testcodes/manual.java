public class manual {

  public void TestMe() {
    int x = 30;
    int y = 10;
    int z = 15;

    if(x == 30) {
      if(y == 10) {
        if(z == 15) {
          System.out.print("X = 30 and Y = 10 and Z == 15");
        }
      }
    }
    if(x > 0){
      if(x < 35){
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
          }
          else if(z < 30){
            System.out.print("4");;
          }
        }
      }
      else if(x > 35){
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