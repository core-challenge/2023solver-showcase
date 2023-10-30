/**
 * Solver
 * アイデア: 遷移列が長い(3桁以上?)の場合、解集合を列挙する方法ではTimeoutする？
 * => 遷移列が短い例での性能をある程度確保しつつ、解集合を列挙せず遷移を予測したい
 */
import java.util.List;
import java.util.ArrayList;
import java.util.Queue;
import java.util.Comparator;
import java.util.LinkedList;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.PrintWriter;

// A*アルゴリズムが使える？

public class SimpleSolver {
  /** breadth-first search */
  private static String testPath = "2022benchmark/";
  private static File testFile = new File(testPath + "list/list-debug-benchmark.csv");
  public static void main(String[] args){
    if (args.length == 0) {
      System.out.println("Testrun");
      try (Scanner s = new Scanner(testFile)) {
        while (s.hasNextLine()) {
          String fileStr = s.nextLine();
          String[] files = fileStr.split(",");
          String col = testPath + files[0];
          String dat = testPath + files[1];

          long start = System.currentTimeMillis();
          solve(col, dat);
          long end = System.currentTimeMillis();
          System.out.println("runtime: " + (end - start) + "ms");
        }
      } catch (FileNotFoundException e) {
        e.printStackTrace(); 
      }
    } else if (args[0].endsWith(".col") && args[1].endsWith(".dat")) {
      solve(args[0], args[1]);
    }
    else System.err.println("ArgumentError: 2 Arguments are expected: .col file and .dat file");
  }


  
  protected static void solve(String colPath, String datPath) {
    File col = new File(colPath);
    File dat = new File(datPath);

    /* Load graph structure datas */
    int nodeNum = 0, edgeNum = 0;
    List<boolean[]> adjacentTable = null;
    TokenPlace tokenPlace = null;
    List<Integer> goalTokenPlace = null;

    try(Scanner scol = new Scanner(col); Scanner sdat = new Scanner(dat)) {
      String[] datas;

      // token info
      datas = sdat.nextLine().split(" ");
      int tokenNum = datas.length - 1;

      List<Integer> tp = new ArrayList<>(tokenNum);
      for (String t: datas) {
        if (!t.equals("s")) tp.add(Integer.parseInt(t)-1);
      }
      tp.sort(new Comparator<Integer>() {
        public int compare(Integer a, Integer b) {
          return (a > b)? 1: -1;
        }
      });
      tokenPlace = new TokenPlace(tp);

      datas = sdat.nextLine().split(" ");
      goalTokenPlace = new ArrayList<>(tokenNum);
      for (String t: datas) {
        if (!t.equals("t")) goalTokenPlace.add(Integer.parseInt(t)-1);
      }
      goalTokenPlace.sort(new Comparator<Integer>() {
        public int compare(Integer a, Integer b) {
          return (a > b)? 1: -1;
        }
      });

      // Check the number of vertices and edges
      datas = scol.nextLine().split(" ");
      while (!datas[0].equals("p")) {
        datas = scol.nextLine().split(" ");
      }
      nodeNum = Integer.parseInt(datas[1]);
      edgeNum = Integer.parseInt(datas[2]);

      // Compose adjacent table
      adjacentTable = new ArrayList<>(nodeNum-1);
      for (int i=0; i < nodeNum-1; i++) adjacentTable.add(new boolean[nodeNum-1-i]);
      while (scol.hasNext()) {
        datas = scol.nextLine().split(" ");
        if (datas[0].equals("e")) {
          int t = Integer.parseInt(datas[1])-1;
          int h = Integer.parseInt(datas[2])-1;
          if (t < h) adjacentTable.get(t)[h-1-t] = true;
          else adjacentTable.get(h)[t-1-h] = true;
        }
      }

    } catch(FileNotFoundException e) {
      e.printStackTrace();
    }
    
    // print info
    // System.out.println("Vertices:" + nodeNum + ", Edges:" + edgeNum);

    /* reconfiguration */
    List<List<Integer>> reconfSeq = reconfiguration(tokenPlace, goalTokenPlace, adjacentTable);

    /* print result */
    String output = outputFormat(tokenPlace.place(), goalTokenPlace, reconfSeq);
    System.out.println(output);
    try (PrintWriter pw = new PrintWriter("answer.out")) {
      pw.write(output);
    } catch (Exception e) {
      e.printStackTrace();
    }
    
  }

  protected static List<List<Integer>> reconfiguration(TokenPlace tokenPlace, List<Integer> goalTokenPlace, List<boolean[]> adjacentTable) {
    List<List<Integer>> reconfSeq = new ArrayList<>(1000);
    List<TokenPlace> tokenLog = new ArrayList<>(10000){{add(tokenPlace);}};
    Queue<TokenPlace> tokenPlaceQueue = new LinkedList<>(){{add(tokenPlace);}};
    reconf: while (!tokenPlaceQueue.isEmpty()) {
      TokenPlace tp = tokenPlaceQueue.poll();
      List<List<Integer>> aroundTokenList = composeAroundTokenList(tp, adjacentTable);
      List<int[]> tokenJumps = searchTokenJumps(tp, aroundTokenList);
      for (int[] tj: tokenJumps) {
        TokenPlace jumped = null;
        for (int i = 0; i < tp.place().size(); i++) {
          jumped = new TokenPlace(tp);
          if (jumped.place().get(i) == tj[0]) {
            jumped.place().set(i, tj[1]);
            jumped.place().sort(new Comparator<Integer>() {
              public int compare(Integer a, Integer b) {
                return (a > b)? 1: -1;
              }
            });
            break;
          }
        }
        if (jumped.place().equals(goalTokenPlace)) {
          reconfSeq = composeSeq(jumped);
          break reconf;
        }
        if (contain(tokenLog, jumped)) continue;
        else {
          tokenLog.add(jumped);
          tokenPlaceQueue.add(jumped); 
        }
      }
    }
    // System.out.println("Found Independent Sets: " + tokenLog.size());
    return reconfSeq;
  }
  
  protected static List<List<Integer>> composeAroundTokenList(TokenPlace tokenPlace, List<boolean[]> adjacentTable) {
    List<List<Integer>> aroundTokenList = new ArrayList<>(adjacentTable.size()+1);
    for (int i = 0; i < adjacentTable.size()+1; i++) aroundTokenList.add(new ArrayList<>(tokenPlace.place().size()));
    for (int t: tokenPlace.place()) {
      aroundTokenList.get(t).add(t);
      for (int i=0; i < adjacentTable.size(); i++) {
        if (i == t) {
          for (int j = 0; j < adjacentTable.get(t).length; j++) {
            if (adjacentTable.get(t)[j]) aroundTokenList.get(j+1+i).add(t);
          }
          break;
        } else {
          if (adjacentTable.get(i)[t-1-i]) aroundTokenList.get(i).add(t);
        }
      }
    }
    return aroundTokenList;
  }
    
  protected static List<int[]> searchTokenJumps(TokenPlace tokenPlace, List<List<Integer>> aroundTokenList) {
    List<int[]> tokenJumps = new ArrayList<>(tokenPlace.place().size()*(aroundTokenList.size()-1));
    for (int i = 0; i < aroundTokenList.size(); i++) {
      List<Integer> at = aroundTokenList.get(i);
      if (at.size() == 1 && at.get(0) != i) {
        tokenJumps.add(new int[]{at.get(0), i});
      } else if (at.size() == 0) {
        for (int t: tokenPlace.place()) tokenJumps.add(new int[]{t, i});
      }
    }
    return tokenJumps;
  }

  public static List<List<Integer>> composeSeq(TokenPlace tp) {
    if (tp.parent() == null) return new ArrayList<>(){{add(tp.place());}};
    List<List<Integer>> reconfSeq = new ArrayList<>(composeSeq(tp.parent()));
    reconfSeq.add(tp.place());
    return reconfSeq;
  }

  public static String outputFormat(List<Integer> initTokenPlace, List<Integer> goalTokenPlace, List<List<Integer>> reconfSeq) {
    String s = "";
    s += "s";
    for (int t: initTokenPlace) s += " " + String.valueOf(t+1);
    s += "\nt";
    for (int t: goalTokenPlace) s += " " + String.valueOf(t+1);
    s += "\na ";
    if (reconfSeq.isEmpty()) s += "NO";
    else {
      s += "YES";
      for (List<Integer> tp: reconfSeq) {
        s += "\na";
        for (int t: tp) {
          s += " " + String.valueOf(t+1);
        }
      }
    }
    
    return s;
  }

  public static boolean contain(List<TokenPlace> tpl, TokenPlace tokenPlace) {
    for (TokenPlace tp: tpl) {
      if (tp.place().equals(tokenPlace.place())) return true;
    }
    return false;
  }
  
}