package com.lyy.demo1

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Properties
import java.sql.DriverManager
import org.ansj.app.summary.SummaryComputer
import org.ansj.app.keyword.KeyWordComputer
import org.ansj.recognition.impl.StopRecognition
import org.ansj.splitWord.analysis.NlpAnalysis
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.joda.time.DateTime

import scala.collection.mutable

object Util {

  val connectionProperties = new Properties()
  connectionProperties.put("user", "root")
  connectionProperties.put("password", "123456")
  val url = "jdbc:mysql://localhost:3306/opinion?serverTimezone=Asia/Shanghai"

  def conn(spark:SparkSession,table_name:String):DataFrame={
    val article_DF = spark.read
      .jdbc(url = url, table = table_name, connectionProperties)
//            .show(20)
    article_DF
  }

  def save(df:DataFrame,table_name:String,saveMode:String):Unit={
    df.write.mode(saveMode)
      .jdbc(url, table_name, connectionProperties)
  }

  def ansj_split_word(str:String):String={
    import scala.collection.JavaConversions.asJavaCollection
    val src = scala.io.Source.fromFile("src/main/resources/library/stop.dic")
    val stops = src.getLines().toList
    val filter = new StopRecognition()
    filter.insertStopWords(stops)
    filter.insertStopNatures("w")//过滤掉标点
    val result = NlpAnalysis.parse(str).recognition(filter)
      .toStringWithOutNature(" ")
     result
  }

  def convert_date(str:String):String={
    val dt = str.split(" ")(0)
//    val sdf = new SimpleDateFormat("yyyy-MM-DD")
//    val dtime = new java.sql.Date(sdf.parse(str).getTime)
    dt
  }

  def convert_to_date(str:String):java.sql.Date={
    val sdf = new SimpleDateFormat("yyyy-MM-DD")
    val dtime = new java.sql.Date(sdf.parse(str).getTime)
    dtime
  }

  def sen_analysis(str:String):Int={
    val filter = new StopRecognition()
    filter.insertStopNatures("w")
    val words = NlpAnalysis.parse(str).recognition(filter).toStringWithOutNature(" ").split(" ")
//      .toStringWithOutNature(" ")
    var score = 0.0
    val dic=  new mutable.HashMap[String,Double]()
    val f = scala.io.Source.fromFile("src/main/resources/library/sentiment.txt")
    f.getLines().foreach{x=>
      val arr = x.split(" ")
//      dic(arr(0))=arr(1).toFloat
      if (arr.length==2){
        dic(arr(0))=arr(1).toDouble
      }
    }
//    dic.foreach(println)
    words.foreach{word=>
      score = score + dic.getOrElse(word,0.0)
//      println(word + " " +dic.getOrElse(word,0.0))
    }
    var sentiment = 0
    if (score>50) sentiment = 1
    else if (score> -10) sentiment =2
    sentiment
  }

  def top_word(title:String,content:String):String={
    val kws = new KeyWordComputer(5)
    val result = kws.computeArticleTfidf(title,content).toArray()
      .map(x=>x.toString.split("/")(0)).mkString(" ")
    result
  }

//  repaet：转发数 comment：评论数 like：点赞数
  def heat_compute(reapeat:Int,comment:Int,like:Int):Double={
    reapeat * 0.5 + comment * 0.3 + like *0.2
  }

  def ex_abstract(title:String,content:String):String={
    val summary = new SummaryComputer(25, title, content).toSummary()
    val result = summary.getSummary
    result + "..."
  }

  def delete_table(table_name:String):Unit={
    val myUrl = "jdbc:mysql://localhost/opinion?serverTimezone=Asia/Shanghai"
    val conn = DriverManager.getConnection(myUrl, connectionProperties)
    val query = "delete from " + table_name
    val preparedStmt = conn.prepareStatement(query)
    preparedStmt.execute
  }

  def main(args: Array[String]): Unit = {
//    val str = "286条红线，划出一个垃圾分类模范村"
//    println(sen_analysis(str))
//    val kws = new KeyWordComputer(5)
    val  title = "2019篮球世界杯抽签规则公布 中国锁定A组在北京打小组赛"
    val  content = "北京时间3月16日，2019年篮球世界杯抽签仪式将在深圳拉开帷幕，届时32支球队分组结果将公布。今日，国际篮联公布了抽签规则，作为东道主，中国男篮将避开其他7个种子队。另外，国际篮协表示，在与赛事组委会协商之后达成一致：中国队将锁定落位在A组，并在北京开始篮球世界杯的小组赛。而卫冕冠军美国队，则锁定E组，从上海开始他们的篮球世界杯之旅。首先来了解下基本信息：本届世界杯扩军为32支球队，所有球队分为8档，除了东道主中国，其他球队都按照世界排名来确定属于哪一档。中国同世界第1位的美国、世界第2位的西班牙和世界第3位的法国同属于第一档，剩下的28支球队则根据各自的世界排名分布到相应的档。值得一提的是，今年有一个变化，分组时要避免有两支来自美洲的球队在同一组，多米尼加、波多黎各、美国和委内瑞拉会分布到A、C、E、G组，加拿大的归档则从第五档调整到了第六档，他们跟伊朗换了位置。视频：3分钟解读男篮世界杯分组规则2019篮球世界杯32强被分为8档本届篮球世界杯具体抽签规则如下：32支球队分为A、B、C、D、E、F、G、H这8个小组，每个小组包含4支球队。为了平衡每个小组的实力——不仅仅是首轮，还包括第二轮——抽签时要遵循以下原则，第一档、第四档、第五档和第八档的球队分到A、C、E、G组。第二档、第三档、第六档和第七档的球队则分到B、D、F、H组。第一档：四支球队（中国、美国、西班牙、法国）将会被分到A、C、E、G组，在同赛事组委会协商后确定，东道主中国将会进入A组，比赛在北京进行。卫冕冠军美国将会被分到E组，比赛在上海进行。第二档：四支球队（塞尔维亚、阿根廷、立陶宛、希腊）将会被分到B、D、F、H组。第三档：四支球队（俄罗斯、澳大利亚、巴西、意大利）也会被分到B、D、F、H组，但根据规定，巴西不能跟阿根廷同组。第四档：四支球队（波多黎各、土耳其、多米尼加、委内瑞拉）被分到A、C、E、G组，三支美洲波多黎各、多米尼加和委内瑞拉不能与美国队同组。第五档：四支球队（德国、伊朗、捷克、波兰）将会被分到A、C、E、G组，但来自亚洲的伊朗队不能与中国同组。第六档：四支球队（加拿大、黑山、菲律宾、韩国）会被分到B、D、F、H组，但加拿大不能被分到阿根廷或巴西那一组，菲律宾和韩国也不能被分到澳大利亚那一组。第七档：四支球队（尼日利亚、塞内加尔、新西兰、安哥拉）被分到B、D、F、H组，新西兰不能跟其他亚洲球队一组。第八档：剩下的日本、约旦、突尼斯、科特迪瓦被分到剩下的小组中，日本和约旦不能被分到中国或者伊朗所在的小组。按照安排，A组的比赛在北京进行，B组的比赛在武汉进行，C组在广州进行，D组在佛山进行，E组在上海进行，F组在南京，G组在深圳，H组在东莞。推荐阅读：为何杜兰特缺阵，火箭反输勇士？点击“阅读原文”，查看篮球世界杯专题"
    //    val result = kws.computeArticleTfidf(title,content).toArray().map(x=>x.toString.split("/")(0)).mkString(" ")
//    println(result)
    val summary = new SummaryComputer(40, title, content).toSummary()
    val result = summary.getSummary
    println(result+"...")
//     val a=1
//     val b=2
//     val c=3
//     val result = heat_compute(a,b,c)
//     println(result)
  }
}
