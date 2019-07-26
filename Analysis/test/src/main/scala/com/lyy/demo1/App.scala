package com.lyy.demo1


import org.apache.spark.sql.SparkSession

/**
 * Hello world!
 *
 */

object App {
  def main(args: Array[String]): Unit = {
//    println( "Hello World!" )
      val spark = SparkSession
        .builder()
        .appName("Spark SQL test")
        .config("spark.some.config.option", "some-value")
        .master("local[3]")
        .getOrCreate()
//    读入new_article表，创建全局视图
      val article_DF =Util.conn(spark,"new_article")
      article_DF.createOrReplaceTempView("article")


//    his_article 表分析
//      spark.sql("select * from article").groupBy("keyword","website").count().show()
//    分词测试
      spark.udf.register("split",Util.ansj_split_word _)

//    情感测试
      spark.udf.register("sen_analysis",Util.sen_analysis _)
//      spark.sql("select sen_analysis(content) as sentiment from article").show(50)

//    主题词测试
      spark.udf.register("top_word",Util.top_word _)
//      spark.sql("select top_word(title,content) as top_word from article").show(20)

//    热度测试
      spark.udf.register("heat",Util.heat_compute _)
//      spark.sql("select heat(repeat1,comment,like1) as heat from article").show(50)

//    摘要测试
      spark.udf.register("ex_abs",Util.ex_abstract _)
//      spark.sql("select ex_abs(title,content) as abstract from article").show(100)

//    相似文章数测试
//       略
//    分析之后存入his_article表
      val history_DF = spark.sql("select title,author,keyword,website,url,split(content) as content," +
        "pub_time,crawl_time,source,ex_abs(title,content) as abstract,sen_analysis(content) as sentiment," +
        "top_word(title,content) as top_word,heat(repeat1,comment,like1) as heat from article")
      Util.save(history_DF,"his_article","append")


//    清空new_article表测试
      Util.delete_table("new_article")

//    读入his_article表，创建全局视图
      val his_article_DF =Util.conn(spark,"his_article")
      his_article_DF.createOrReplaceTempView("article")



//    web_distribute 表分析
      val web_distribute = spark.sql("select keyword,website from article")
        .groupBy("keyword","website").count()
      Util.save(web_distribute,"web_distribute","overwrite")

//    sen_proportion 表分析
      val sen_pro = spark.sql("select keyword,sentiment from article")
        .groupBy("keyword","sentiment").count()
      Util.save(sen_pro,"sen_proportion","overwrite")

//    hot_news 热点文章
      val hot_news = spark.sql("SELECT url,keyword,abstract FROM article ORDER BY heat DESC LIMIT 200")
      Util.save(hot_news,"hot_news","overwrite")


//    word_cloud 表分析



////  spread_tend 表分析
      spark.udf.register("convert",Util.convert_date _)
      val time_DF = spark.sql("select keyword,website,convert(pub_time) as date from article")
        .groupBy("keyword","website","date").count()
//  //  切记视图已经切换
      time_DF.createOrReplaceTempView("spread_tend")
      spark.udf.register("convert_to_date",Util.convert_to_date _)
      val spread_tend = spark.sql("select keyword,website,convert_to_date(date) " +
        "as date,count from spread_tend")
  //    spread_tend.printSchema()
      Util.save(spread_tend,"spread_tend","overwrite")

//      切回his_article视图
        his_article_DF.createOrReplaceTempView("article")


//    sen_tend 表分析
      spark.udf.register("convert",Util.convert_date _)
      val sen_time_DF = spark.sql("select keyword,sentiment,convert(pub_time) as date from article")
        .groupBy("keyword","sentiment","date").count()
//      切记视图已经切换
      sen_time_DF.createOrReplaceTempView("sen_tend")
      spark.udf.register("convert_to_date",Util.convert_to_date _)
      val sen_tend = spark.sql("select keyword,sentiment,convert_to_date(date) " +
        "as date,count from sen_tend")
        //    spread_tend.printSchema()
      Util.save(sen_tend,"sen_tend","overwrite")

    //
      spark.stop()

  }
}
