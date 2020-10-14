import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;

public abstract class ComplexPricing implements ISalePricing{
    private List<ISalePricing> pricings = new ArrayList<ISalePricing>();

    public ComplexPricing(ISalePricing pricing){
        if (pricing == null){
            throw new NullPointerException();
        }
        pricings.add(pricing);
    }

    public void add(ISalePricing pricing){
        if (pricing == null){
            throw new NullPointerException();
        }
        pricings.add(pricing);
    }
    public List<ISalePricing> getPricings(){
        return pricings;
    }
}
