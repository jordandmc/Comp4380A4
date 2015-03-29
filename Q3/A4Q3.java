import java.io.*;
import java.util.*;
import java.lang.*;

public class A4Q3
{
  public static int studPgSize = 0;
  public static int enrldPgSize = 0;
  public static int studCol = 0;
  public static int enrldCol = 0;
  public static int numBuff = 0;
  public static int studPgs = 0;
  public static int enrldPgs = 0;
  
    public static void main (String [] args)
    {
      ArrayList<ArrayList<String>> joinTable = null;
      ArrayList<ArrayList<String>> studentTable = new ArrayList<ArrayList<String>>();
      ArrayList<ArrayList<String>> enrolledTable = new ArrayList<ArrayList<String>>();
      studentTable.add(new ArrayList<String>());
      enrolledTable.add(new ArrayList<String>());
      
      studentTable = readInRecords(studentTable, args[0]);
      
      enrolledTable = readInRecords(enrolledTable, args[1]);
      
      readInInfo(args[2]);
      printIntroInfo(studentTable.size(), enrolledTable.size());
            
      joinTable = joinTables(studentTable, enrolledTable);
      printTable(joinTable);
    }
    
    public static ArrayList<ArrayList<String>> readInRecords(ArrayList<ArrayList<String>> table, String textFile)
    {
      String[] split;
       try
        {
            BufferedReader fileIn = new BufferedReader( new FileReader (textFile) );
            String line = fileIn.readLine();
            int lineCnt = 0;
            while ( line != null )
            {
                split = line.split("\\s+");
                
                
                table.add(new ArrayList<String>());
                
                for(int i = 0; i < split.length; i++)
                {
                  table.get(lineCnt).add(split[i]);
                }
                
                line = fileIn.readLine();
                lineCnt++;
            }
        }
        catch(IOException ioe)
        {
            ioe.printStackTrace();
        }
        
        return table;
    }
    
    public static void readInInfo(String textFile)
    {
      try
      {
        BufferedReader fileIn = new BufferedReader( new FileReader (textFile) );
        String line = fileIn.readLine();
        int lineCnt = 0;
        String[] split;
        
        split = line.split("\\s+");
        studPgSize = Integer.parseInt(split[2]);
        
        line = fileIn.readLine();
        split = line.split("\\s+");
        enrldPgSize = Integer.parseInt(split[2]);
        
        line = fileIn.readLine();
        split = line.split("\\s+");
        studCol = Integer.parseInt(split[2]);
        enrldCol = Integer.parseInt(split[3]);
        
        line = fileIn.readLine();
        split = line.split("\\s+");
        numBuff = Integer.parseInt(split[1]); 
      }
       catch(IOException ioe)
        {
            ioe.printStackTrace();
        }
    }
    
    public static void printTable(ArrayList<ArrayList<String>> table)
    {
      for(int i = 0; i<table.size(); i++)
      {
        for(int j = 0; j<table.get(i).size(); j++)
        {
          System.out.print(table.get(i).get(j) + " ");
        }
        System.out.println();
      }
    }
    
    public static void printIntroInfo(int numStuds, int numEnrld)
    {
      studPgs = (int)Math.ceil((double)numStuds/studPgSize);
      enrldPgs = (int)Math.ceil((double)numEnrld/enrldPgSize);
      
      System.out.println("With page size=" + studPgSize + " records per page, N1=" + numStuds +
                         " records in Students.txt can fit into P1=" + studPgs +
                         " pages.");
      System.out.println("With page size=" + enrldPgSize + " records per page, N2=" + numEnrld +
                         " records in Enrolled.txt can fit into P2=" + enrldPgs +
                         " pages.");
      System.out.println("The common columns are Column 1 in Students.txt and Column 1 in Enrolled.txt.");
      
      System.out.println("These records are joined using the Simple Nested Loop Join with B=" +
                         numBuff + " pages.");
    }
    
    public static ArrayList<ArrayList<String>> joinTables(ArrayList<ArrayList<String>> studTable, ArrayList<ArrayList<String>> enrldTable)
    {
      int startStud = 0;
      int startEnrld = 0;
      int endStud = studPgSize;
      int endEnrld = enrldPgSize;
      String enrldId = "";
      String studId = "";
      ArrayList<ArrayList<String>> joinTable = new ArrayList<ArrayList<String>>();
      
      for(int k=0; k<studPgs; k++)
      {
        for(int i=0; i<enrldPgs; i++)
        {
          for(int j=studPgSize*k; j<studTable.size()-1 && j<studPgSize*(k+1); j++)
          {
            for(int l=enrldPgSize*i; l<enrldTable.size()-1 && l<enrldPgSize*(i+1); l++)
            {
              enrldId = enrldTable.get(l).get(0);
              studId = studTable.get(j).get(0);
              
               if(enrldId.equals(studId))
               {
                 joinTable = addToJoinTable(joinTable, enrldTable.get(l), studTable.get(j));
               }
            } 
          }
        } 
      }      
      return joinTable;
    }
    
    public static ArrayList<ArrayList<String>> addToJoinTable(ArrayList<ArrayList<String>> joinTable, ArrayList<String> enrldRecord, ArrayList<String> studRecord)
    {
      ArrayList<String> newRecord = new ArrayList<String>();
      
      newRecord.add(studRecord.get(0));
      newRecord.add(studRecord.get(1));
      newRecord.add(enrldRecord.get(1));
      newRecord.add(enrldRecord.get(2));
      newRecord.add(enrldRecord.get(3));
      
      joinTable.add(newRecord);
      
      return joinTable;
    }
}