import java.util.Scanner;

public class io {
    public static void print(String var0) {
        System.out.println(var0);
    }

    public static String input() {
        Scanner var0 = new Scanner(System.in);
        String var1;
        try {
            var1 = var0.nextLine();
        } catch (Throwable var4) {
            try {
                var0.close();
            } catch (Throwable var3) {
                var4.addSuppressed(var3);
            }
            throw var4;
        }
        var0.close();
        return var1;
    }

    public static String int2str(int var0) {
        return String.valueOf(var0);
    }

    public static int str2int(String var0) {
        return Integer.parseInt(var0);
    }

    public static String float2str(float var0) {
        return String.valueOf(var0);
    }

    public static float str2float(String var0) {
        return Float.parseFloat(var0);
    }

    public static String bool2str(boolean var0) {
        return String.valueOf(var0);
    }

    public static boolean str2bool(String var0) {
        return Boolean.parseBoolean(var0);
    }
}
