public abstract class Material {
    private String name;
    private double price;

    public Material(String name, double price) {
        if(name == null){
            throw new NullPointerException();
        }
        if(name == ""){
            throw new IllegalArgumentException();
        }
        if(price <0){
            throw new IllegalArgumentException();
        }
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPricePerUnit() {
        return price;
    }

    public abstract int getMaterialRequirements(Surface surface);

    public double getPriceOfASurface(Surface surface) {
        if(surface == null){
            throw new NullPointerException();
        }
        int requirements = this.getMaterialRequirements(surface);
        return requirements * price;
    }
}