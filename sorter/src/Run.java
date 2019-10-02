import java.util.ArrayList;
import java.util.Arrays;

public class Run {

    public static void main(String[] args) throws Exception {
        String filename = args[0];
        boolean rowSort = (args[1] == "r" || args[1] == "R");
        Sorter s = new Sorter(filename);
        if (rowSort) {
            s.MSBradixSort();
        }
        else {
            s.columnRadixSort();
            metaData(s.getMatrix());
        }
        s.writeToFile("sorted" + filename);
    }

    //produces metadata for
    private static void metaData(char[][] matrix) {
        System.out.println("Super sets:");
        boolean[] isSubset = new boolean[matrix[0].length];
        for (int col=  matrix[0].length -1; col > 0; col--) {
            ArrayList<Integer> subsets = new ArrayList<>();
            for (int prev = col - 1; prev >= 0; prev --) {
                if (!isSubset[col]) {
                    boolean subset = true;
                    for (int i=0; i< matrix.length; i++) {
                        if (matrix[0][prev] == Sorter.ONE) {
                            if (matrix[0][col] == Sorter.ZERO) {
                                subset = false;
                            }
                        }
                    }
                    if (subset) {
                        isSubset[prev] = true;
                        subsets.add(prev);
                    }
                }
            }
            if (!subsets.isEmpty()) {
                System.out.println("Column " + col + " has subsets: " + subsets.toString());
            }
        }

    }
}
