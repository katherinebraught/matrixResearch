import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Sorter {
    private char[][] organisms;

    public static final char ZERO = '-';
    public static final char ONE = 'X';

    public Sorter(String fileName) throws Exception {
        readInFile(fileName);
    }

    public char[][] getMatrix() {
        return organisms;
    }

    private void readInFile(String filename) throws Exception {
        File f = new File(filename);
        Scanner s = new Scanner(f);

        ArrayList<String> tempOrganisms = new ArrayList<>();

        while (s.hasNext()) {
            String name = s.next();
            String availability = s.next();
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
        arr[i] = arr[j];
        arr[j] = temp;
    }

    private void swapColumn(char[][] arr, int i, int j) {
        char[] temp = new char[arr.length];
        for (int k=0; k < arr.length; k++) {
            temp[k]= arr[k][i];
        }
        for (int k=0; k < arr.length; k++) {
            arr[k][i] = arr[k][j];
        }
        for (int k=0; k < arr.length; k++) {
            arr[k][j] = temp[k];
        }
    }

    public void MSBradixSort() {
        int m = organisms.length;
        MSBradixSortRec(0, m, 0, organisms);
    }

    private void MSBradixSortRec(int start, int end, int index, char[][] organisms) {
        if (index == organisms[0].length || end - start == 1) {
            return;
        }
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
        MSBradixSortRec(start, zeroBinEnd, index +1, organisms);
        MSBradixSortRec(oneBinStart, end, index +1, organisms);
    }

    public void columnRadixSort() {
        int m = organisms[0].length;
        columnRadixSortRec(0, m, 0, organisms);

    }

    private void columnRadixSortRec(int start, int end, int index, char[][] organisms) {
        if (index == organisms.length || end - start == 1) {
            return;
        }
        int zeroBinEnd = start;
        int oneBinStart = end;
        int i = start;
        while (zeroBinEnd != oneBinStart) {
            if (organisms[index][i] == ONE) {
                oneBinStart -= 1;
                swapColumn(organisms, i, oneBinStart);
            }
            else {
                zeroBinEnd += 1;
                i++;
            }
        }
        columnRadixSortRec(start, zeroBinEnd, index +1, organisms);
        columnRadixSortRec(oneBinStart, end, index +1, organisms);
    }


}
