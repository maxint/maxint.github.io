---
layout: page
title: Categories
group: navigation
premalink: /categories/
---

{% include JB/setup %}

<div class="tag_box">
	<ul>
		{% assign tags_list = site.categories %}  
		{% include JB/tags_list %}
	</ul>
</div>

{% for tag in site.categories %} 
  <h3 id="{{ tag[0] }}-ref" class="title">{{ tag[0] }}</h3>
  {% assign pages_list = tag[1] %}  
  {% include JB/pages_list %}
{% endfor %}
