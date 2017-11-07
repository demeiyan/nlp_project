import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * dmyan2017/11/6
 **/
public class Test {
    public static void main(String[] args){
/*        System.out.print("输入句子 : ");
        Scanner sc = new Scanner(System.in);
        String[] inputs  = sc.nextLine().split("\\s");
        for(String input:inputs){
            System.out.println(input+input.length());
        }*/
/*        String pattern = "[^\\u4e00-\\u9fa5]+";
        Pattern p =Pattern.compile(pattern);
        String str = "MQ-8C,";
        System.out.println(str.matches(pattern));

        System.out.println(str.substring(0,str.length()));*/
        String str = "“詹森-杜汉”";
        String spec = "[`~!@#$%^&*()+=|{}':;',\\[\\].<>/?~！@#￥%……&*（）\\-——+|{}【】‘；：”“’。，、？]";
        System.out.println(str.replaceAll(spec,""));

    }
}
