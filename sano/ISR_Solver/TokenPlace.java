import java.util.List;
import java.util.ArrayList;

public class TokenPlace {
  private int depth;
  private TokenPlace parent = null;
  private List<Integer> tokenPlace;

  // For initial tokenplace
  public TokenPlace(List<Integer> tokenPlace) {
    this.tokenPlace = new ArrayList<>(tokenPlace);
    this.depth = 0;
  }

  // For transition
  public TokenPlace(TokenPlace tokenPlace) {
    this.parent = tokenPlace;
    this.tokenPlace = new ArrayList<>(tokenPlace.place());
    this.depth = tokenPlace.depth + 1;
  }

  public boolean equals(TokenPlace tp) {
    return this.tokenPlace.equals(tp.tokenPlace);
  }

  public int depth() {
    return depth;
  }

  public TokenPlace parent() {
    return parent;
  }

  public List<Integer> place() {
    return tokenPlace;
  }
  
}
