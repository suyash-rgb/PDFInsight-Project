package package1;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.util.*;

import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

public class PDFTextMatcherTest {

    @Test
    public void testProcessPDF() throws IOException {
        // Mock data for testing
        String filePath = "test.pdf";  // Ensure you have a test PDF named "test.pdf" for this test
        List<String> referenceList = Arrays.asList("Java", "Python", "Ruby");

        // Since processPDF doesn't return anything, we need to assert based on side effects
        // Usually, we'd modify the method to return some testable result, but for now, we'll rely on manual verification.
        PDFTextMatcher.processPDF(filePath, referenceList);
        
        // No assertions here, but you should check the console output for expected results
    }

    @Test
    public void testTokenizeText() {
        String text = "Java JavaScript Python";
        Map<String, Integer> tokenCountMap = PDFTextMatcher.tokenizeText(text);
        assertEquals(3, tokenCountMap.size());
        assertEquals(2, (int) tokenCountMap.get("Java"));
        assertEquals(1, (int) tokenCountMap.get("Python"));
    }

    @Test
    public void testMatchValues() {
        Map<String, Integer> tokenCountMap = new HashMap<>();
        tokenCountMap.put("Java", 2);
        tokenCountMap.put("Python", 1);
        tokenCountMap.put("JavaScript", 3);

        List<String> referenceList = Arrays.asList("Java", "Python", "Ruby");
        Map<String, Integer> matchedWords = new HashMap<>();

        int matches = PDFTextMatcher.matchValues(tokenCountMap, referenceList, matchedWords);

        assertEquals(2, matches);
        assertEquals(2, (int) matchedWords.get("Java"));
        assertEquals(1, (int) matchedWords.get("Python"));
    }

    @Test
    public void testCalculateMatchPercentage() {
        int matches = 3;
        int referenceListLength = 5;
        double matchPercentage = PDFTextMatcher.calculateMatchPercentage(matches, referenceListLength);
        assertEquals(60.0, matchPercentage);
    }
}
