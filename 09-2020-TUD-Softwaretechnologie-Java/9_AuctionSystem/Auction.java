import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public abstract class Auction {
    private boolean closed;
    private List<Person> bidders = new ArrayList<>();
    private List<Item> allItems = new ArrayList<>();

    public Auction() {
    }

    public void addBid(Item bidItem, String nameOfBidder, long price){
        if(closed == true){
            throw new IllegalStateException();
        }
        if(nameOfBidder=="" || price <= 0){
            throw new IllegalArgumentException();
        }
        if(nameOfBidder==null || bidItem == null){
            throw new NullPointerException();
        }
        System.out.println("bidders: "+bidders);
        if(allItems.contains(bidItem)) {
            Person newBider = new Person(nameOfBidder);
            bidders.add(newBider);
            bidItem.addBid(newBider, price);
        }
        else{
            throw new NoSuchElementException();
        }
    }

    public String closeAuction(){
        if(closed ==true)
            if(closed == true) {
                throw new IllegalStateException();
            }
        closed =  true;
        return generateItemListString();
    }

    public String generateAllBidsString(Item item){
        if(item == null){
            throw new NullPointerException();
        }
        else{
            String string = "All bids:\n";
            System.out.println("item: "+item);
            System.out.println("item.getAllBids():"+item.getAllBids());
            for(Bid bid : item.getAllBids()){
                string = string + bid.toString() + "\n";
            }
            return string;
        }
    }

    public String generateItemListString(){
        String string = "";
        for (Item item : allItems){
            string = string + (generateItemString(item) + "\n");
        }
        return string;
    }

    public void registerItem(Item item){
        if(item == null){
            throw new NullPointerException();
        }
        if (closed == true){
            throw new IllegalStateException();
        }
        for(Item itemL : allItems){
            if(itemL.getName() == item.getName()){
                throw new IllegalArgumentException();
            }
        }
        allItems.add(item);
    }

    public abstract String generateItemString(Item item);

    public List<Item> getAllItems(){
        return allItems;
    }
}
