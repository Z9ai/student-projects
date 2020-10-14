import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class DefaultCollector implements KeywordCollector{

    @Override
    public Set<String> getKeywords(Resource res) {
        String keyword = res.getType().getDescription();
        Set<String> keywords = new HashSet<>();
        keywords.add(keyword);
        return keywords;
    }
}