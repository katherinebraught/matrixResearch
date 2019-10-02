import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Arrays;

public class Results {

    //contains the cross referenced list for each taxon/gene
    private Node[][] matrix;

    //contains the colors a taxon has
    ArrayList<Node> taxons;
    //contains the colors a gene is missing
    ArrayList<Node> genes;


    enum Color
    {
        RED, GREEN, BLUE, YELLOW;
    }


    public Results(String filename, String originalMatrixFile, String outputFile ) throws Exception {
        readFile(filename);
        setUpMatrix();
        produceOutput(originalMatrixFile, outputFile);
    }

    private void produceOutput(String originalMatrixFile, String outputFile) throws Exception {
        File taxons = new File(originalMatrixFile);
        File outFile = new File(outputFile);
        FileWriter out = new FileWriter(outFile);
        Scanner s = new Scanner(taxons);
        int row = 0;
        while (s.hasNext()) {
            String taxonName = s.next() + " " + s.next();
            s.next();
            if (!taxonName.equals("")) {
                out.write(taxonName + " ");
                out.write(Arrays.toString(matrix[row]));
                out.write("\n");
                row++;
            }
        }
        if (row < matrix.length - 1) {
            out.write("warning: miss matched data and taxon name count. Data may be missing");
        }
        out.close();
        s.close();
    }

    private void setUpMatrix() {
        matrix = new Node[taxons.size()][genes.size()];
        for (int i = 0; i< matrix.length; i++) {
            for (int j=0; j< matrix[0].length; j++) {
                Node temp = new Node();
                temp.setBlue(taxons.get(i).isBlue() && !genes.get(j).isBlue());
                temp.setRed(taxons.get(i).isRed() && !genes.get(j).isRed());
                temp.setGreen(taxons.get(i).isGreen() && !genes.get(j).isGreen());
                temp.setYellow(taxons.get(i).isYellow() && !genes.get(j).isYellow());
                matrix[i][j] = temp;
            }
        }
    }

    private void readFile(String filename) throws Exception {
        taxons = new ArrayList<>();
        genes = new ArrayList<>();
        File f = new File(filename);
        Scanner s = new Scanner(f);
        s.nextLine(); //skip the formatting line
        while (s.hasNext()) {
            String data = s.next();
            String valueString = s.next();
            int value = Integer.parseInt(valueString);
            String[] parts = data.split("[(,)]");
            if (parts[0].equals("x")) {
                int taxonIndex = Integer.parseInt(parts[1]);
                int color = Integer.parseInt(parts[2]);
                boolean hasColor = (true ? (value == 1) : false);
                //place into the array
                if (taxons.size() <= taxonIndex) {
                    taxons.add(taxonIndex, new Node().setColor(color, hasColor));
                }
                else {
                    taxons.get(taxonIndex).setColor(color, hasColor);
                }

            }
            if (parts[0].equals("z")) {
                int column = Integer.parseInt(parts[1]);
                int color = Integer.parseInt(parts[2]);
                boolean missingColor = (true ? (value == 1) : false);
                if (genes.size() <= column) {
                    genes.add(column, new Node().setColor(color, missingColor));
                }
                else {
                    genes.get(column).setColor(color, missingColor);
                }

            }
        }
        s.close();
    }

    private class Node {
        boolean red;
        boolean green;
        boolean blue;
        boolean yellow;

        public String toString() {
            String result = "[";
            result += (red ? "R" : " ");
            result += (green ? "G" : " ");
            result += (blue ? "B" : " ");
            result += (yellow ? "Y" : " ");
            result += "]";
            return result;
        }

        public Node setColor(int color, boolean value) {
            if (color == 0) {
                red = value;
            }
            if (color == 1) {
                green = value;
            }
            if (color == 2) {
                blue = value;
            }
            if (color == 3) {
                yellow = value;
            }
            return this;
        }


        public void setRed(boolean red) {
            this.red = red;
        }

        public void setGreen(boolean green) {
            this.green = green;
        }

        public void setBlue(boolean blue) {
            this.blue = blue;
        }

        public void setYellow(boolean yellow) {
            this.yellow = yellow;
        }

        public boolean isRed() {
            return red;
        }

        public boolean isGreen() {
            return green;
        }

        public boolean isBlue() {
            return blue;
        }

        public boolean isYellow() {
            return yellow;
        }
    }
}
