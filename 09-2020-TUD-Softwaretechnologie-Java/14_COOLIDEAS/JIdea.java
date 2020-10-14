import java.util.ArrayList;
import java.util.List;

public class JIdea extends JContent{
    public List<JAttachment> attachments = new ArrayList();
    private JState state = new Draft();

    public JIdea(String title, String description) {
        super(title, description);
        if(title == null|| description == null){
            throw new NullPointerException();
        }
        if(title == ""|| description == ""){
            throw new IllegalArgumentException();
        }
    }

    public void discuss(String text){
        if(text == null){
            throw new NullPointerException();
        }
        if(text == ""){
            throw new IllegalArgumentException();
        }
        state.discuss(text);
    }

    public void evaluate(JValuation valuation){
        if(valuation == null){
            throw new NullPointerException();
        }
        state.evaluate(valuation);
    }

    public void hold(){
        state.hold();
    }

    public void release(){
        state.release();
    }

    public void decline(){
        state.decline();
    }

    public boolean isDeclined(){
        if(state instanceof DeclinedIdea){
            return true;
        }
        return false;
    }

    public boolean isReleased(){
        if(state instanceof ReleasedIdea){
            return true;
        }
        return false;
    }

    public String getCurrentDiscussion(){
        return state.getCurrentDiscussion();
    }

    public JValuation getValuation(){
        return state.getValuation();
    }

    public void addAttachment(JAttachment attachment){
        if(attachment == null){
            throw new NullPointerException();
        }
        this.attachments.add(attachment);
    }

    public List<JAttachment> getAttachments(){
        return this.attachments;
    }

    public boolean removeAttachment(JAttachment attachment){
        if(attachment == null){
            throw new NullPointerException();
        }
        return this.attachments.remove(attachment);
    }

    @Override
    public String toString() {

        return String.format("Idea: %s\n%s",super.getTitle(),super.getDescription());
    }









    public abstract class JState{
        private String currentDiscussion = "";
        private JValuation valuation;

        public void discuss(String text){
            if(text == null){
                throw new NullPointerException();
            }
            throw new IllegalStateException();
        }

        public void evaluate(JValuation valuation){
            if(valuation == null){
                throw new NullPointerException();
            }
            throw new IllegalStateException();
        }

        public void hold(){
            throw new IllegalStateException();
        }

        public void release (){
            throw new IllegalStateException();
        }

        public void decline (){
            throw new IllegalStateException();
        }

        public void setCurrentDiscussion(String currentDiscussion) {
            if(currentDiscussion == null){
                throw new NullPointerException();
            }
            if(currentDiscussion == ""){
                throw new IllegalArgumentException();
            }
            this.currentDiscussion = currentDiscussion;
        }

        public void setValuation(JValuation valuation) {
            if(valuation == null){
                throw new NullPointerException();
            }
            this.valuation = valuation;
        }

        public String getCurrentDiscussion() {
            return currentDiscussion;
        }

        public JValuation getValuation() {
            return valuation;
        }
    }




    public class Draft extends JState{
        public void hold(){
            state = new OpenDraft();
        }

        public void decline(){
            state = new DeclinedIdea();
        }
    }


    public class OpenDraft extends JState{

        public void discuss(String text){
            String newDiscussion = super.getCurrentDiscussion()  + text + "\n";
            super.setCurrentDiscussion(newDiscussion);
        }
        public void evaluate(JValuation valuation){
            super.valuation = valuation;
        }

        public void hold(){
            state = new ApprovedIdea();
        }

        public void decline(){
            state = new DeclinedIdea();
        }
    }



    public class ApprovedIdea extends JState{
        public void release(){
            state = new ReleasedIdea();
        }
    }


    public class ReleasedIdea extends JState{

    }


    public class DeclinedIdea extends JState{

    }
}
