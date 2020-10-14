public class EndsWith implements Predicate<String> {
    private String suffix;

    public EndsWith(String suffix){
        if(suffix == null){
            throw new IllegalArgumentException();
        }
        this.suffix = suffix;
    }

    public boolean test(String value){  //dem parameter wird dann später das iter.. objekt übergeben, dies wird dann mit dem suffix verglichen
        if(value == null){
            return false;
        }
        int valueIndex = value.length()-1;
        int suffixIndex = suffix.length()-1;
        if (suffix.length()>value.length()){
            return false;
        }
        for(int i=0; i<suffix.length(); i++) {
            if (suffix.charAt(suffixIndex) != value.charAt(valueIndex)) {
                return false;
            }
            valueIndex = valueIndex -1;
            suffixIndex = suffixIndex -1;
        }
        return true;
    }
}
