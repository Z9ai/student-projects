import java.util.Iterator;

public class TextFileIterator implements Iterator<String> {
    
    public TextFileIterator(Resource res){
        this.getAsString(res);
    }

    @Override
    public boolean hasNext() {
    }

    @Override
    public String next(){
    }

    @Override
    public void remove(){
        throw new UnsupportedOperationException();
    }

    public String getAsString(Resource res){
        return "We wish you good luck in this exam!\nWe hope you are well pre-\npared.";
    }
}
