import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 英文单词词性还原
 * dmyan 2017/11/4
 *
 **/
public class Token {
	
	@SuppressWarnings({ "unused", "resource","unchecked" })
	public static void main(String[] args) throws IOException {


		Map<String,String> map = new HashMap();
		Map<String,String> patternMap = new HashMap<>();
		//String pattern  = "^\\w"+"("+""+")?";
        BufferedReader br;
        String s ;
        String[] strs = {};
        br  = new BufferedReader(new InputStreamReader(Token.class.getResourceAsStream("rule.txt")));
        for(s=br.readLine();s!=null;s=br.readLine()){

            strs = s.split("->");
            //System.out.println(strs.toString());
            patternMap.put(strs[0].replaceAll("\\*","").trim(),strs[1].replaceAll("\\*","").trim());
        }
        //String pattern = "("+strs[0].trim()+")$";
        List<String>  patterns = new ArrayList<>();

        for(String e :patternMap.keySet()){
            patterns.add("("+e+")$");
        }
        br = new BufferedReader(new InputStreamReader(Token.class.getResourceAsStream("dic_ec.txt")));

		try {
			int i;
			for(s=br.readLine();s!=null;s=br.readLine()){
				//s="hello    world";
				strs = s.split("");
				s= "";
				for(i = 1;i<strs.length;i++){
					s += strs[i]+" ";
				}
				map.put(strs[0], s);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		br.close();
		String[] inputs ={"1"};
		String find = null;
		while(!inputs[0].equals("0")){
			System.out.print("输入待查询的单词： ");
			Scanner sc = new Scanner(System.in);
            inputs  = sc.nextLine().split(" ");
			String token= "";
			for(String input:inputs){
                token=(find=map.get(input.trim()))+"";
				if(find == null){
				    Pattern p;
				    Matcher m;
				    String group,instead;
				     for (String pattern :patterns){
                         p = Pattern.compile(pattern);
                         m = p.matcher(input);
                         if(m.find()){
                             group = m.group();
                             instead = patternMap.get(pattern.substring(1,pattern.length()-2));
                             if(instead.contains("/")){
                                if((!(token=map.get(input.substring(0,m.start())+instead.split("/")[0])+"").trim().equals( "null"))||(!(token=map.get(input.substring(0,m.start())+instead.split("/")[1])+"").trim().equals( "null")))
                                {break;}
                             }else if(instead.contains("?")){
                                if(input.charAt(m.start())==input.charAt(m.start()+1)){
                                    if(!(token=map.get(input.substring(0,m.start())+input.charAt(m.start()))+"").trim().equals( "null")){break;}
                                }
                             }else {
                                 if(!(token=map.get(input.substring(0,m.start())+instead)+"").trim().equals( "null")){break;}
                             }
                         }

                     }
                    if(token.trim().equals("null")){
                        BufferedWriter out = null;
                        URL url = Token.class.getResource("");
                        String str=url.toString();
                        out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(str.substring(str.indexOf("/")+1)+"dic_ec.txt"), true)));
                        out.write("\r\n"+input+"\t未登录词块");
                        //System.out.println("词典中没有该词444 !");
                        out.close();
                    }
				}
			}
			if(!token.trim().equals("null")){
				System.out.println("查询结果为："+token);
			}else{
				System.out.println("词典中没有该词 !");
			}
					
		}
		br.close();
	}
}
