package package1;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class PDFTextMatcher {

    // Reads PDF and processes content in chunks
    public static void processPDF(String filePath, List<String> referenceList) throws IOException {
        PDDocument document = PDDocument.load(new File(filePath));
        PDFTextStripper pdfStripper = new PDFTextStripper();

        int totalMatches = 0;
        Map<String, Integer> matchedWords = new HashMap<>();

        int totalPages = document.getNumberOfPages();
        for (int i = 1; i <= totalPages; i++) {
            pdfStripper.setStartPage(i);
            pdfStripper.setEndPage(i);
            String text = pdfStripper.getText(document);
            
            Map<String, Integer> tokenCountMap = tokenizeText(text);
            totalMatches += matchValues(tokenCountMap, referenceList, matchedWords);
        }
        
        document.close();
        
        double matchPercentage = calculateMatchPercentage(totalMatches, referenceList.size());
        outputResult(matchedWords, matchPercentage, referenceList);
    }

    // Tokenizes text into words and counts occurrences
    public static Map<String, Integer> tokenizeText(String text) {
        String[] tokens = text.split("\\W+");
        Map<String, Integer> tokenCountMap = new HashMap<>();
        for (String token : tokens) {
            tokenCountMap.put(token, tokenCountMap.getOrDefault(token, 0) + 1);
        }
        return tokenCountMap;
    }

    // Matches token counts with reference list and updates matched words count
    public static int matchValues(Map<String, Integer> tokenCountMap, List<String> referenceList, Map<String, Integer> matchedWords) {
        int matches = 0;
        for (String word : referenceList) {
            if (tokenCountMap.containsKey(word)) {
                matches++;
                matchedWords.put(word, matchedWords.getOrDefault(word, 0) + tokenCountMap.get(word));
            }
        }
        return matches;
    }

    // Calculates match percentage
    public static double calculateMatchPercentage(int matches, int referenceListLength) {
        return ((double) matches / referenceListLength) * 100;
    }

    // Outputs results
    public static void outputResult(Map<String, Integer> matchedWords, double matchPercentage, List<String> referenceList) {
        System.out.println("Provided Reference List: " + referenceList);
        System.out.println("Matched Words: " + matchedWords.keySet());
        System.out.println("Word Occurrences: " + matchedWords);
        System.out.printf("Match Percentage: %.2f%%%n", matchPercentage);
    }

    public static void main(String[] args) {
        try {
            String filePath = "Suyash - professional-resume5.pdf";
            List<String> referenceList = Arrays.asList("Amazon web services cloud", "JavaScript", "Python with ML", "Pandas", "Django Framework");
            processPDF(filePath, referenceList);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}