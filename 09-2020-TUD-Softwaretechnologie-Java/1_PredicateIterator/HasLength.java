public class HasLength implements Predicate<String>{
    private int length;

    public HasLength(int length){
        if(length < 0){
            throw new IllegalArgumentException();
        }
        this.length = length;
    }

    public boolean test(String value){
        if(value == null){
            return false;
        }
        if (length == value.length()){
            return true;
        }
        return false;
    }
}
