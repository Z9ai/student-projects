import java.io.File;

public class JAttachment extends JContent{
    private File file;

    public JAttachment(String title, String description, File file) {
        super(title, description);
        if(file == null || description == null || title == null){
            throw new NullPointerException();
        }
        if(title == "" || description == ""){
            throw new IllegalArgumentException();
        }
        this.file = file;
    }

    public File getFile() {
        return file;
    }

    public void setFile(File file) {
        if(file == null){
            throw new NullPointerException();
        }
        this.file = file;
    }

    @Override
    public String toString() {
        return String.format("Attachment: %s\n%s",super.getTitle(),super.getDescription());
    }
}
