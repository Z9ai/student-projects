import java.util.ArrayList;
import java.util.List;

public class Item {
    private String name;
    private String description;
    private long minPrice;
    private List<Bid> allBids = new ArrayList<>();
    private Bid highestBid;

    public Item(String name, String description, long minPrice) {
        if(name == null || description == null){
            throw new NullPointerException();
        }
        if(name == "" || description == ""){
            throw new IllegalArgumentException();
        }
        if(minPrice <= 0){
            throw new IllegalArgumentException();
        }
        this.name = name;
        this.description = description;
        this.minPrice = minPrice;
    }

    public void addBid(Person bidder, long price){
        if(bidder == null){
            throw new NullPointerException();
        }
        if(price <= 0){
            throw new IllegalArgumentException();
        }
        System.out.println(bidder);
        System.out.println(allBids);
        System.out.println("price" + price);
        System.out.println("minPrice" +minPrice);
        if(allBids == null){
            allBids = new ArrayList<>();
        }
        if(price >= minPrice){
            System.out.println(price+" >= " +minPrice);
            if(allBids.isEmpty()) {
                highestBid = new Bid(bidder, price);
                allBids.add(highestBid);
            }
            else if(price > highestBid.getPrice()) {
                highestBid = new Bid(bidder, price);
                allBids.add(highestBid);
            }
        }
    }

    public List<Bid> getAllBids() {
        return allBids;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public Bid getHighestBid() {
        return highestBid;
    }

    @Override
    public String toString() {
        return name + ": " + description + " (minimum bidding price: " + minPrice + " EUR)";
    }
}
