public class Flooring extends Material{
    private static double limit = 0.02;
    private double widthOfFlooring;

    public Flooring(String name, double price, double width){
        super(name,price);
        if(width <= 0 || price < 0){
            throw new IllegalArgumentException();
        }
        this.widthOfFlooring = width;
    }

    public double getWidth() {
        return widthOfFlooring;
    }

    public int getMaterialRequirements(Surface surface){
        if(surface == null){
            throw new NullPointerException();
        }
        double notRounded;
        int rounded;
        notRounded = surface.getArea()/widthOfFlooring;
        rounded = (int) (Math.floor(notRounded-limit) + 1);
        return rounded;
    }
}