<?php
 return [
  'name' => 'employment',
  'label' => 'Beschäftigung',
  'info' => '',
  'type' => 'collection',
  'fields' => [
    0 => [
      'name' => 'name',
      'type' => 'text',
      'label' => 'Name',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'multiline' => false,
        'showCount' => true,
        'readonly' => false,
        'placeholder' => NULL,
        'minlength' => NULL,
        'maxlength' => NULL,
        'list' => NULL,
      ],
    ],
    1 => [
      'name' => 'company',
      'type' => 'contentItemLink',
      'label' => 'Unternehmen',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'link' => 'company',
        'filter' => NULL,
      ],
    ],
    2 => [
      'name' => 'person',
      'type' => 'contentItemLink',
      'label' => 'Person',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'link' => 'person',
        'filter' => NULL,
      ],
    ],
  ],
  'preview' => [
  ],
  'group' => '',
  'meta' => NULL,
  '_created' => 1764891319,
  '_modified' => 1764891319,
  'color' => NULL,
  'revisions' => false,
];