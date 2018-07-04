---
layout: page
title: Tags
group: navigation
premalink: /tags/
---

{% include JB/setup %}

<div class="tag_box">
	<ul>
		{% assign tags_list = site.tags %}  
		{% include JB/tags_list %}
	</ul>
</div>

{% for tag in site.tags %} 
  <h3 id="{{ tag[0] }}-ref" class="title">{{ tag[0] }}</h3>
  {% assign pages_list = tag[1] %}  
  {% include JB/pages_list %}
{% endfor %}
