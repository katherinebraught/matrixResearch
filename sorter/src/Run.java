import java.util.Arrays;
public class Run {

    public static void main(String[] args) throws Exception {
        //String[] organisms = {"--X--", "X---X", "XXXX-", "X--X-"};
        //Sorter s = new Sorter(args[1]);
        //Sorter s = new Sorter("C:\\Users\\Katherine\\IdeaProjects\\matrixResearch\\sorter\\src\\Euphorbia");
        //s.MSBradixSort();
        //System.out.println(Arrays.toString((s.getOrganisms())));
        //s.writeToFile("C:\\Users\\Katherine\\IdeaProjects\\matrixResearch\\sorter\\src\\Euphorbia.sortedd");

        Sorter s = new Sorter("C:\\Users\\Katherine\\IdeaProjects\\matrixResearch\\sorter\\src\\test");
        s.columnRadixSort();
        s.writeToFile("C:\\Users\\Katherine\\IdeaProjects\\matrixResearch\\sorter\\src\\testtColumnSort");

    }
}
