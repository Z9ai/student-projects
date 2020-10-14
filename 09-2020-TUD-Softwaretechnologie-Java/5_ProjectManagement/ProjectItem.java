public abstract class ProjectItem {
    private String name;
    private String details;
    private double rate;

    public ProjectItem(String name, String details, double rate) {
        if(name == "" || details == "" ){
            throw new IllegalArgumentException();
        }
        if(name == null || details == null ){
            throw new NullPointerException();
        }
        if(rate <= 0){
            throw new IllegalArgumentException();
        }
        this.name = name;
        this.details = details;
        this.rate = rate;
    }

    public void setDetails(String details) {
        if(details == ""){
            throw new IllegalArgumentException();
        }
        this.details = details;
    }

    public long getCostEstimate(){
        return  ((long)  (Math.round(rate*this.getTimeRequired()) )  +this.getMaterialCost());
    }

    public abstract double getTimeRequired();

    public abstract long getMaterialCost();

}