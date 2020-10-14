import java.lang.Exception;

public class UnpayableEmployeeException extends Exception{

    public UnpayableEmployeeException(String message) {
        super(message);
    }
}
