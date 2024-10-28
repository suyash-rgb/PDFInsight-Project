package package1;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.util.*;

class PDFTextMatcherTest {

    @Test
    void testReadPDF() throws IOException {
        String text = PDFTextMatcher.readPDF("BrianMason_Using_Rest_API-2.pdf");
        assertNotNull(text);
        assertTrue(text.length() > 0);
    }

    @Test
    void testTokenizeText() {
        String text = "This is a test.";
        Map<String, Integer> tokens = PDFTextMatcher.tokenizeText(text);
        assertEquals(4, tokens.size());
        assertTrue(tokens.containsKey("This"));
        assertEquals(1, (int) tokens.get("This"));
    }

    @Test
    void testMatchValues() {
        Map<String, Integer> tokens = new HashMap<>();
        tokens.put("SOAP", 2);
        tokens.put("Swagger", 1);
        tokens.put("Java", 3);
        List<String> referenceList = Arrays.asList("SOAP", "Swagger", "Java", "Python");
        Map<String, Integer> matchedWords = new HashMap<>();
        int matches = PDFTextMatcher.matchValues(tokens, referenceList, matchedWords);
        assertEquals(3, matches);
        assertEquals(3, matchedWords.size());
        assertEquals(2, (int) matchedWords.get("SOAP"));
    }

    @Test
    void testCalculateMatchPercentage() {
        double matchPercentage = PDFTextMatcher.calculateMatchPercentage(3, 4);
        assertEquals(75.0, matchPercentage);
    }
}

