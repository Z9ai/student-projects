public class Paint extends Material{
    private static double limit = 0.02;
    private int numberOfCoats;
    private double squareMetersPerLiter;

    public Paint(String name, double price, int numberOfCoats, double squareMetersPerLiter) {
        super(name, price);
        if(numberOfCoats <= 0 || squareMetersPerLiter <= 0){
            throw new IllegalArgumentException();
        }
        this.numberOfCoats = numberOfCoats;
        this.squareMetersPerLiter = squareMetersPerLiter;
    }

    public int getNumberOfCoats() {
        return numberOfCoats;
    }

    public double getSquareMetersPerLiter() {
        return squareMetersPerLiter;
    }

    public int getMaterialRequirements(Surface surface){
        if(surface == null){
            throw new NullPointerException();
        }
        double litres = 0;
        int buckets = 0;
        litres = surface.getArea()*numberOfCoats/squareMetersPerLiter;
        buckets = (int) (((litres - limit) +0.5)/ 0.5);
        return buckets;
    }
}