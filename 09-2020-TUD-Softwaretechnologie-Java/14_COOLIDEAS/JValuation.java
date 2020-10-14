public class JValuation extends JContent{

    public JValuation(String title, String description) {
        super(title, description);
    }

    public String toString(){
        return String.format("Valuation: %s\n%s" ,super.getTitle(), super.getDescription());
    }
}
