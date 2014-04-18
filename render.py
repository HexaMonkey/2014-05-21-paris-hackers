#!/usr/bin/env python

import codecs
import re
import jinja2
import markdown
import sys

if (len(sys.argv) != 1):
    sys.stderr.write(" takes .md and template.html as input and produces .html");
    sys.exit(1);

md_file = "slides.md";
authors = [];
website = "";
def gen_contact():
    ret = "<ul>";
    for author in authors:
        ret += "<li>" + author + "</li>";
    if (website != ""):
        ret += "<li>" + website + "</li>";
    ret += "</ul>";
    return ret;
    
def gen_toc(toc, title):
    ret = "<ol>";
    for section in toc:
        if (section == title):
            c = " class=highlighted-section";
        else:
            c = "";

        ret += "<li" + c + ">" + section + "</li>";
    ret += "</ol>";
    return ret;
        
def process_slides():
  with codecs.open('index.html', 'w', encoding='utf8') as outfile:
    md = codecs.open(md_file, encoding='utf8').read()
    md_slides = md.split('\n---\n')
    print 'Compiled %s slides.' % len(md_slides)

    slides = []
    toc = []
    # Process each slide separately.
    slideno = 0;
    for md_slide in md_slides:
      slide = {}
      sections = md_slide.split('\n\n')
      # Extract metadata at the beginning of the slide (look for key: value)
      # pairs.
      metadata_section = sections[0]
      metadata = parse_metadata(metadata_section)
      if ("authors" in metadata):
          global authors;
          authors = metadata["authors"].split(",");
          del(metadata["authors"]);
      if ("website" in metadata):
          global website;
          website = metadata["website"];
          del(metadata["website"]);
      slide.update(metadata)
      remainder_index = metadata and 1 or 0
      # Get the content from the rest of the slide.
      content_section = '\n\n'.join(sections[remainder_index:])
      html = markdown.markdown(content_section)
      slide['content'] = postprocess_html(html, metadata)
      slide['no'] = slideno;
      if ('section' in slide):
        toc.append(slide['section']);
      if (len(toc) > 0):
        slide['section'] = toc[-1];
      else:
        slide['section'] = "--";
      slides.append(slide)
      slideno += 1;

    # generate toc and segue
    for slide in slides:
        if (not 'class' in slide):
            continue;
        
        if (slide['class'].find("toc") != -1):
            section = "";
            if ('section' in slide):
                section = slide['section'];
            slide['content'] = gen_toc(toc, section);
        
    # use title of the first slide as main html title
    title = slides[0]["title"]
    template = jinja2.Template(open('template.html').read(), autoescape=True)

    outfile.write(template.render(locals()))

def parse_metadata(section):
  """Given the first part of a slide, returns metadata associated with it."""
  metadata = {}
  metadata_lines = section.split('\n')
  for line in metadata_lines:
    colon_index = line.find(':')
    if colon_index != -1:
      key = line[:colon_index].strip()
      val = line[colon_index + 1:].strip()
      metadata[key] = val

  return metadata

def postprocess_html(html, metadata):
  """Returns processed HTML to fit into the slide template format."""
  if metadata.get('build_lists') and metadata['build_lists'] == 'true':
    html = html.replace('<ul>', '<ul class="build">')
    html = html.replace('<ol>', '<ol class="build">')
  html = html.replace("<contact/>", gen_contact());
  return html

if __name__ == '__main__':
  process_slides()
