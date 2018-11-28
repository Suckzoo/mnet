public class manual3 {
  public void TestMe() {
    int a = 0;
    int b = 1;
    int c = 2;
    int d = 3;
    int x = 23;
    int y = 24;
    int z = 25;
    if(a == b && c == d){
      if(a > 0 || b < 0){
        if(x > 9){
          System.out.println("Hello");
        }
        else if(x > y || y < z){
          System.out.prinln("Hi");
        }
      }
      else if(a > c && b > d && x == y || z > a){
        if(a > 0){
          if(x + y > 0){
            System.out.prinln("Ni Hao");
          }
          else if(x - y > 0){
            System.out.prinln("Gonnichiwa");
          }
        }
        else if(a == 0){
          if(a + b - c < 0){
            if(d * c == a / b){
              System.out.prinln("zdrastbuize");
            }
            else if(((b + d) - c) * a == 0){
              if(a == 0){
                if(x == 23){
                  System.out.prinln("Buona Sera");
                }
                else{
                  System.out.prinln("Buon Journo");
                }
              }
            }
            System.out.prinln("Annyeong");
          }
        }
      }
    }
  }
}