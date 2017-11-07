import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

/**
 * 基于规则和词典的分词(正向最大匹配FMM)
 * dmyan 2017/11/4
 *
 **/
public class Seg {
    public static void main(String[] args) throws IOException {
        Set<String> sets = new HashSet();
        BufferedReader br = new BufferedReader(new InputStreamReader(Token.class.getResourceAsStream("dict_seg.txt")));
        List<String> segs;
        sets.add("，");
        sets.add(",");
        sets.add("；");
        sets.add(";");
        sets.add("。");
        sets.add(".");
        sets.add("！");
        sets.add("!");
        sets.add("？");
        sets.add("?");
        sets.add("：");
        sets.add(":");
        try {
            String s;
            String[] strs;
            int i;
            for(s=br.readLine();s!=null;s=br.readLine()){
               //System.out.println(s);
                strs = s.split(",");
                if(!sets.contains(strs[0].trim())){
                    sets.add(strs[0].trim());
                }
            }
            br.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        String[] inputs ={"1"};
        int  length = 0 ;
        String pattern = "[^\\u4e00-\\u9fa5]+";//非中文正则
        String pruc = "[\\pP\\p{Punct}]";//标点符号正则
        String spec = "[`~!@#$%^&*()+=|{}':;',\\[\\].<>/?~！@#￥%……&*（）\\-——+|{}【】‘；：”“’。，、？]";//特殊字符正则
        while(!inputs[0].equals("0")){
            System.out.print("输入句子 : ");
            Scanner sc = new Scanner(System.in);
            segs = new ArrayList();
            inputs  = sc.nextLine().split("\\s");
            for(String input:inputs){
                length = input.length();
                while(input.length()>0){
                    length = input.length();
                    for(int i = length;i>=0;){
                        if(input ==null ||input.length()<=0)break;
                        if(input.substring(0,i).matches(pattern)||input.substring(0,i).matches(pruc)||input.substring(0,i).matches(spec)||sets.contains(input.substring(0,i))){
                            segs.add(input.substring(0,i));
                            input = input.substring(i,input.length());
                            //System.out.println(input);
                            i = input.length();
                        }else{
                            i--;
                        }
                    }
                    if(input.length()>0){
                        segs.add(input.charAt(0)+"");
                        input = input.substring(1,input.length());
                    }
                }
            }
            System.out.print("分词结果 : ");
            for(String seg:segs){
                System.out.print(seg+" ");
            }
            System.out.println();
        }

    }
}
