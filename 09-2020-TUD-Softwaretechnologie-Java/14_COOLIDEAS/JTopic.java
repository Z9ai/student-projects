public class JTopic extends JContent {
    private int id;

    public JTopic(String title, String description, int id) {
        super(title, description);
        if(title == null|| description == null){
            throw new NullPointerException();
        }
        if(title == ""|| description == ""){
            throw new IllegalArgumentException();
        }
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public String toString(){
        return String.format("Topic: %s\n%s",super.getTitle(), super.getDescription());
    }
}
