// example for tast 1

public class Valid {
	public void testMe(int x, int y) {
		int x2 = x - y;
		int x3 = x + y;
		assert(x2 + x3 - x == x); // assertion is so valid
	}
}
