import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


public class A4Q2 {
	public static void main(String[] args) throws IOException {
		List<Integer> sIDs = new ArrayList<Integer>();
		String fileNameToRead = null;
		String fileNameToWrite = null;
		String pageSize = null;
		String buffPages = null;
		if(args.length > 0){

			pageSize = args[0];
			buffPages = args[1];
			
			fileNameToRead = args[2];
			fileNameToWrite = args[3];
		}


		sIDs  = readFile(fileNameToRead);
		mergeSort(sIDs, fileNameToWrite,pageSize,buffPages);



	}// main
	private static void  mergeSort(List<Integer> ListToSort, String fileName, String pageSize, String buffPages) throws IOException{
		List<Integer> subListToSort = new ArrayList<Integer>();
		List<List<Integer>> listOLists = new ArrayList<List<Integer>>();
		
		double pgSize =  Double.parseDouble(pageSize);
		double numOfBuffPgs =  Double.parseDouble(buffPages);
		double numOfsIDs = 0;
		double sIDsToRead = 0;
		double numOfPgs = 0;
		double numOfPass = 0;
		int from = 0;
		int to = 0;


		numOfsIDs = ListToSort.size();
		numOfPgs = Math.ceil(numOfsIDs/pgSize);
		sIDsToRead = numOfBuffPgs * pgSize;
		numOfPass = Math.ceil(1 +(Math.log(Math.ceil(numOfPgs/numOfBuffPgs)) / Math.log(numOfBuffPgs-1)));

		for (int i = 0; i < numOfPass;i++){
			System.out.println("Pass "+i);
			from = 0;
			to = 0;
			if(i == 0){

				for(to = 0 ; to != numOfsIDs ; ){
					from = to;
					to = (int) (to+sIDsToRead);

					if (to > numOfsIDs){
						to = (int) (numOfsIDs % sIDsToRead);
						to += from;
					}
					subListToSort = new ArrayList<Integer>();
					subListToSort = ListToSort.subList(from, to);
					System.out.println("Read "+subListToSort);
					Collections.sort(subListToSort);
					System.out.println("Write "+subListToSort);
					listOLists.add( subListToSort);
				}

			}else{

				for(int j = 0; j < listOLists.size();){
					System.out.print("Read ");
					subListToSort = new ArrayList<Integer>();
					for(int k = 0; k < numOfBuffPgs-1 && j < listOLists.size() ; k++, j++){
						System.out.print(listOLists.get(j));
						subListToSort.addAll(listOLists.get(j));
						listOLists.remove(j);
						j--;
					}
					Collections.sort(subListToSort);
					System.out.println();
					System.out.println("Write "+subListToSort);
					listOLists.add(0,subListToSort);
					j++;

				}
			}
			System.out.println();
		}
		FileWriter fw = new FileWriter(fileName,false);
		BufferedWriter bw = new BufferedWriter(fw);
		subListToSort = listOLists.get(0);
		for (int k = 0; k < subListToSort.size(); k++){
			bw.write(subListToSort.get(k).toString());
			bw.newLine();

		}
		bw.close();


	}
	private static List<Integer>  readFile(String string ) throws IOException {
		FileInputStream fis = new FileInputStream(string);
		List<Integer> SIDList = new ArrayList<Integer>();
		//Construct BufferedReader from InputStreamReader
		BufferedReader br = new BufferedReader(new InputStreamReader(fis));

		String line = null;
		while ((line = br.readLine()) != null) {

			SIDList.add(Integer.parseInt(line));
		}

		br.close();
		return SIDList;
	}
}// class StreamClient

