public abstract class Part {
    private String id;
    private String name;

    public Part(String id, String name) {
        if (id == null || name == null){
            throw new NullPointerException();
        }
        if (id == ""  || name  == ""){
            throw new IllegalArgumentException();
        }
        this.id = id;
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}
