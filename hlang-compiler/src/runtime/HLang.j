.source HLang.java
.class public HLang
.super java/lang/Object

.method public static processArray([II)I
.var 0 is data [I from Label0 to Label1
.var 1 is multiplier I from Label0 to Label1
Label0:
.var 2 is sum I from Label0 to Label1
	iconst_0
	istore_2
.var 3 is i I from Label0 to Label1
	iconst_0
	istore_3
Label2:
	iload_3
	iconst_3
	if_icmpge Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifle Label3
Label6:
	iload_2
	aload_0
	iload_3
	iaload
	iload_1
	imul
	iadd
	istore_2
	iload_3
	iconst_1
	iadd
	istore_3
Label7:
	goto Label2
Label3:
	iload_2
	ireturn
Label1:
.limit stack 4
.limit locals 4
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is numbers [I from Label0 to Label1
	iconst_3
	newarray int
	dup
	iconst_0
	iconst_2
	iastore
	dup
	iconst_1
	iconst_4
	iastore
	dup
	iconst_2
	bipush 6
	iastore
	astore_1
.var 2 is factor I from Label0 to Label1
	iconst_3
	istore_2
.var 3 is result I from Label0 to Label1
	bipush 36
	istore_3
	iload_3
	invokestatic io/int2str(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	return
Label1:
.limit stack 5
.limit locals 4
.end method

.method public <init>()V
.var 0 is this LHLang; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method
