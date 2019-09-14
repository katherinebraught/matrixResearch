import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Sorter {
    private char[][] organisms;

    private final char ZERO = '-';
    private final char ONE = 'X';

    public Sorter(String fileName) throws Exception {
        readInFile(fileName);
    }

    public char[][] getOrganisms() {
        return organisms;
    }

    public void readInFile(String filename) throws Exception {
        File f = new File(filename);
        Scanner s = new Scanner(f);

        ArrayList<String> tempOrganisms = new ArrayList<>();

        while (s.hasNext()) {
            String name = s.next();
            String availability = s.next();
            //Data data = new Data(name, availability);
            tempOrganisms.add(availability);
        }

        organisms = new char[tempOrganisms.size()][];
        for (int i = 0; i < tempOrganisms.size(); i++) {
            organisms[i] = tempOrganisms.get(i).toCharArray();
        }

        s.close();

    }

    public void writeToFile(String filename) throws Exception {
        File f = new File(filename);
        FileWriter fw = new FileWriter(f);

        for (int i = 0; i< organisms.length; i++) {
            fw.write(organisms[i], 0, organisms[i].length);
            fw.write('\n');
        }
        fw.close();
    }


    private void printState(char[][] org, int zeroBin, int oneBin) {
        for (int i = 0; i< org.length; i++) {
            if (i == oneBin) {
                System.out.print("\\");
            }
            for (int j =0; j<org[i].length; j++)
                System.out.print(org[i][j]);
            System.out.print(",");

            if (i==zeroBin) {
                System.out.print("|");
            }
        }
        System.out.println();
    }

    private void swap(char[][] arr, int i, int j) {
        char[] temp = Arrays.copyOf(arr[i], arr[i].length);
        //Data temp = new Data(arr[i].getName(), arr[i].getData());
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public void MSBradixSort() {
        int m = organisms.length;
        MSBradixSortRec(0, m, 0, organisms);

    }

    public void MSBradixSortRec(int start, int end, int index, char[][] organisms) {
        if (index == organisms[0].length || end - start == 1) {
            return;
        }
        System.out.println("start " + index);
        int zeroBinEnd = start;
        int oneBinStart = end;
        int i = start;
        while (zeroBinEnd != oneBinStart) {
            printState(organisms, zeroBinEnd, oneBinStart);
            if (organisms[i][index] == ONE) {
                oneBinStart -= 1;
                swap(organisms, i, oneBinStart);
            }
            else {
                zeroBinEnd += 1;
                i++;
            }
        }
        System.out.println("Sort zero bin:" + start + " to "  + zeroBinEnd);
        MSBradixSortRec(start, zeroBinEnd, index +1, organisms);
        System.out.println("Sort one bin:" + oneBinStart + " to " + end);
        MSBradixSortRec(oneBinStart, end, index +1, organisms);
    }

}
