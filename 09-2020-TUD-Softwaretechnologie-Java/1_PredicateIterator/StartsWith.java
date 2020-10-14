public class StartsWith implements Predicate<String>{
    private String prefix;

    public StartsWith(String prefix){
        if(prefix == null){
            throw new IllegalArgumentException();
        }
        this.prefix = prefix;
    }

    public boolean test(String value){  //dem parameter wird dann später das iter.. objekt übergeben, dies wird dann mit dem prefix verglichen
        if(value == null){
            return false;
        }
        if (prefix.length()>value.length()){
            return false;
        }
        for(int i=0; i<prefix.length(); i++) {
            if (prefix.charAt(i) != value.charAt(i)) {
                return false;
            }
        }
        return true;
    }
}
